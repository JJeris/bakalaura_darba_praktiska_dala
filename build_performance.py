import subprocess
import time
import json
import shutil
import argparse
from pathlib import Path
import platform
import psutil
import os

ITERATIONS = 5

def get_cpu_model():
    """Get the CPU model human readable value."""
    try:
        if platform.system() == "Windows":
            output = subprocess.check_output("wmic cpu get Name", shell=True).decode()
            lines = [line.strip() for line in output.splitlines() if line.strip()]
            return lines[1] if len(lines) > 1 else "Unknown"
        else:
            return platform.processor() or "Unknown"
    except Exception as e:
        print(f"Error detecting CPU model: {e}")
        return "Unknown"

def get_system_info():
    """
    Get system info, like CPU, GPU, core and thread count etc.
    Source: https://stackoverflow.com/questions/37825360/determine-what-gpu-is-running-through-wmi
    """
    try:
        cpu = get_cpu_model()
        cores = psutil.cpu_count(logical=False)
        threads = psutil.cpu_count(logical=True)
        ram = f"{round(psutil.virtual_memory().total / (1024**3))} GB"
        os_info = f"{platform.system()} {platform.release()} ({platform.version()})"
        try:
            gpu = subprocess.check_output("wmic path win32_VideoController get name", shell=True).decode()
            gpu = [line.strip() for line in gpu.splitlines() if line.strip()][1]
        except Exception:
            gpu = "Unknown"
        return {
            "os": os_info,
            "cpu": cpu,
            "ram": ram,
            "gpu": gpu,
            "cpu_cores": cores,
            "cpu_threads": threads
        }
    except Exception as e:
        print(f"System info error: {e}")
        return {}

def get_tool_version_with_cmd(cmd):
    """Executes a version retrieval command and return the result."""
    try:
        return subprocess.check_output(cmd, shell=True).decode().strip()
    except Exception:
        return "Unknown"

def get_framework_version_from_package_json(project_type, project_root_directory):
    """Gets projects frameworks version from package.json."""
    package_json_path = os.path.join(project_root_directory, "package.json")
    try:
        with open(package_json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        deps = data.get("dependencies", {})
        dev_deps = data.get("devDependencies", {})
        
        if project_type == "tauri":
            return deps.get("@tauri-apps/api") or dev_deps.get("@tauri-apps/api") or "Unknown"
        elif project_type == "electronjs":
            return deps.get("electron") or dev_deps.get("electron") or "Unknown"
    except Exception:
        return "Unknown"


def get_framework_versions(project_type, project_root_directory):
    """Get the versions for the project used tools."""
    framework_version = get_framework_version_from_package_json(project_type, project_root_directory)
    if project_type == "tauri":
        return {
            "tauri": framework_version,
            "node": get_tool_version_with_cmd("node -v"),
            "npm": get_tool_version_with_cmd("npm -v"),
            "cargo": get_tool_version_with_cmd("cargo --version").replace("cargo ", ""),
            "rust": get_tool_version_with_cmd("rustc --version").replace("rustc ", ""),
        }
    elif project_type == "electronjs":
        return {
            "electron": framework_version,
            "node": get_tool_version_with_cmd("node -v"),
            "npm": get_tool_version_with_cmd("npm -v"),
        }
    else:
        return {
            "node": get_tool_version_with_cmd("node -v"),
            "npm": get_tool_version_with_cmd("npm -v"),
        }


def get_file_size(file_path):
    """Returns the size of the file in bytes."""
    if file_path.exists():
        return file_path.stat().st_size
    return 0

def run_command(cmd, cwd):
    """Executes a given cmd and outputs its stdout to the terminal."""
    
    print(f"\nRunning passed command: {cmd} (in {cwd})")
    start_ms = time.time_ns() // 1_000_000
    proc = subprocess.Popen(cmd, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if proc.stdout:
        for line in proc.stdout:
            print(line, end='')
    
    proc.wait()
    end_ms = time.time_ns() // 1_000_000 # From ns to ms.
    return {
        "cmd": cmd,
        "cwd": str(cwd),
        "start_ms": start_ms,
        "end_ms": end_ms,
        "duration_ms": end_ms - start_ms,
        "success": proc.returncode == 0,
    }
    
def delete_node_modules(project_dir):
    node_modules = Path(project_dir) / "node_modules"
    if node_modules.exists():
        print("Deleting node_modules...")
        shutil.rmtree(node_modules)

def delete_dist(project_dir):
    dist_directory = Path(project_dir) / "dist"
    if dist_directory.exists():
            print("Deleting dist directory...")
            shutil.rmtree(dist_directory)

def get_build_file_sizes(project_type, src_dir, target_type):
    """Gets the file sizes of the .msi and .exe files for the given target type."""
    if target_type == "dev":
        return {
            "msi_size_bytes": 0,
            "exe_size_bytes": 0
        }
        
    if project_type == "tauri":
        msi_path = src_dir / "target" / target_type / "bundle" / "msi" / "blendio-tauri_0.1.0_x64_en-US.msi"
        exe_path = src_dir / "target" / target_type / "blendio-tauri.exe"

        msi_size = get_file_size(msi_path)
        exe_size = get_file_size(exe_path)

        return {
            "msi_size_bytes": msi_size,
            "exe_size_bytes": exe_size
        }
    
    
    elif project_type == "electronjs":
        msi_path = src_dir / "dist" / "blendio-electronjs-1.0.0-installer.msi"
        exe_path = src_dir / "dist" / "win-unpacked" / "blendio-electronjs.exe"

        msi_size = get_file_size(msi_path)
        exe_size = get_file_size(exe_path)

        if target_type == "dist_unpacked":
            return {
                "msi_size_bytes": 0,
                "exe_size_bytes": exe_size
            }
        else:
            return {
                "msi_size_bytes": msi_size,
                "exe_size_bytes": exe_size
            }
    else:
        return {
            "msi_size_bytes": 0,
            "exe_size_bytes": 0
        }
        
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_type", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output_dir", required=False)
    args = parser.parse_args()

    with open(args.config, "r", encoding="utf-8") as f:
        config = json.load(f)

    project_dir = Path(config["project_dir"])
    if args.project_type == "tauri":
        src_dir = project_dir / "src-tauri"
    elif args.project_type == "electronjs":
        src_dir = project_dir

    # Use overridden result dir if given
    if args.output_dir:
        result_dir = Path(args.output_dir)
    else:
        result_dir = Path(config["result_dir"])
    result_dir.mkdir(parents=True, exist_ok=True)

    test_cases = config["tests"]

    for test_case in test_cases:
        print(f"\n=== Running test case: {test_case['result_file_name']} ===")
        all_results = []

        system_info = get_system_info()
        framework_versions = get_framework_versions(args.project_type, project_dir)

        for i in range(ITERATIONS):
            print(f"\n--- Iteration {i+1}/{ITERATIONS} ---")
            session_start_ms = time.time_ns() // 1_000_000
            iteration = {
                "iteration": i + 1,
                "system_info": system_info,
                "framework_versions": framework_versions,
                "session_start_ms": session_start_ms,
                "steps": [],
                "build_commands_used": test_case.get("build_commands", [])
            }

            if (i == 0 and args.project_type == "electronjs") or test_case.get("delete_dist"):
                delete_dist(project_dir)

            if (i == 0 and args.project_type == "tauri") or test_case.get("cargo_clean"):
                iteration["steps"].append(run_command("cargo clean", cwd=src_dir))

            if i == 0 or test_case.get("delete_node_modules"):
                delete_node_modules(project_dir)

            if i == 0 or test_case.get("npm_install"):
                iteration["steps"].append(run_command("npm install", cwd=project_dir))

            for cmd in test_case.get("build_commands", []):
                iteration["steps"].append(run_command(cmd, cwd=project_dir))

            # Get the file sizes of the generated build (MSI, EXE)
            build_sizes = get_build_file_sizes(args.project_type, src_dir, test_case["target_type"])
            iteration.update(build_sizes)

            all_results.append(iteration)

        # Write results to the corresponding test case's file
        result_file = result_dir / test_case["result_file_name"]
        with open(result_file, "w", encoding="utf-8") as f:
            json.dump(all_results, f, indent=2)

        print(f"\nResults saved to {result_file}")

if __name__ == "__main__":
    main()
