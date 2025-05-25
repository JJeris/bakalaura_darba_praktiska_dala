import subprocess
import time
import psutil
import os
import sys
import json
import shutil
import argparse
from pathlib import Path
import platform

ITERATIONS = 10

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


def get_build_file_path(project_type, src_dir, executable_type):
    """Gets the .exe file path."""
    if project_type == "tauri":
        exe_path = src_dir / "target" / executable_type / "blendio-tauri.exe"
        return exe_path
    else:
        exe_path = src_dir / "dist" / "win-unpacked" / "blendio-electronjs.exe"
        return exe_path   

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
    
def convert_bytes_to_mb(bytes_val):
    """Format byes to megabytes."""
    return f"{bytes_val / (1024 * 1024):.2f} MB"

def get_process_memory(p: psutil.Process):
    """Return memory in USS (if available), else RSS"""
    try:
        mem_info = p.memory_full_info()
        return getattr(mem_info, 'uss', p.memory_info().rss)
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return 0

def monitor_runtime_resource_usage(exe_path, duration_seconds=10):
    """Launches the given .exe and logs CPU/RAM usage and process count over time."""
    if not exe_path.exists():
        print(f"Error: Executable not found at {exe_path}")
        return {"error": "Executable not found"}

    try:
        # Launch executable file.
        proc = subprocess.Popen([str(exe_path)])
        print(f"Launched {exe_path.name} with PID {proc.pid}")
        parent = psutil.Process(proc.pid)

        
        parent.cpu_percent(interval=None)
        for child in parent.children(recursive=True):
            child.cpu_percent(interval=None)

        resource_usage_instances = []

        start_ms = int(time.time() * 1000)

        for p in [parent] + parent.children(recursive=True):
            try:
                p.cpu_percent(interval=None)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        interval_seconds = 1
        samples_target = duration_seconds

        for i in range(samples_target):
            iteration_start = time.time()

            try:
                all_procs = parent.children(recursive=True)
                all_procs.insert(0, parent)

                timestamp_ms = int(time.time() * 1000)

                total_ram = 0
                total_cpu = 0.0
                process_count = 0

                for p in all_procs:
                    if not p.is_running():
                        continue
                    try:
                        ram = get_process_memory(p)
                        cpu = p.cpu_percent(interval=None)
                        total_ram += ram
                        total_cpu += cpu
                        process_count += 1
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue

                resource_usage_instances.append({
                    "timestamp_ms": timestamp_ms,
                    "main_pid": parent.pid,
                    "main_name": parent.name(),
                    "ram_bytes": total_ram,
                    "cpu_percent": total_cpu,
                    "process_count": process_count
                })

                print(f"[{timestamp_ms}] {parent.name()} (PID {parent.pid}): "
                    f"{convert_bytes_to_mb(total_ram)} RAM | {total_cpu:.1f}% CPU | {process_count} procs")

            except psutil.NoSuchProcess:
                print("Main process ended.")
                break

            # Sleep just enough to maintain interval
            iteration_duration = time.time() - iteration_start
            time_to_sleep = max(0, interval_seconds - iteration_duration)
            time.sleep(time_to_sleep)

        end_ms = int(time.time() * 1000)
        duration_ms = end_ms - start_ms

        print(f"Finished monitoring after {(duration_ms / 1000):.2f} seconds.")
        # Kill application and its processes.
        try:
            for child in parent.children(recursive=True):
                if child.is_running():
                    child.terminate()
            parent.terminate()

            gone, alive = psutil.wait_procs([parent] + parent.children(recursive=True), timeout=5)
            for p in alive:
                p.kill()
                
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            print(f"Warning: Failed to cleanly terminate processes: {e}")
        
        return {
            "start_ms": start_ms,
            "end_ms": end_ms,
            "duration_ms": duration_ms,
            "success": True,
            "resource_usage_instances": resource_usage_instances
        }

    except Exception as e:
        print(f"Error during monitoring: {e}")
        try:
            for child in parent.children(recursive=True):
                if child.is_running():
                    child.terminate()
            parent.terminate()

            gone, alive = psutil.wait_procs([parent] + parent.children(recursive=True), timeout=5)
            for p in alive:
                p.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            print(f"Warning: Failed to cleanly terminate processes: {e}")
        
        return {
            "start_ms": int(time.time() * 1000),
            "end_ms": int(time.time() * 1000),
            "duration_ms": 0,
            "success": False,
            "error": str(e),
            "resource_usage_instances": []
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
                "build_commands_used": test_case.get("build_commands", [])
            }

            if i == 0:
                run_command("npm install", cwd=project_dir)
            if i == 0:
                for cmd in test_case.get("build_commands", []):
                    run_command(cmd, cwd=project_dir)
        
            build_file_path = get_build_file_path(args.project_type, src_dir, test_case["executable_type"])
            if build_file_path.exists():
                print(f"\nLaunching and monitoring: {build_file_path}")
                usage_result = monitor_runtime_resource_usage(build_file_path, duration_seconds=60)
                iteration["runtime_resource_usage"] = usage_result
            else:
                print(f"Executable not found at {build_file_path}")
            
            all_results.append(iteration)

        # Write results to the corresponding test case's file
        result_file = result_dir / test_case["result_file_name"]
        with open(result_file, "w", encoding="utf-8") as f:
            json.dump(all_results, f, indent=2)

        print(f"\nResults saved to {result_file}")


if __name__ == "__main__":
    main()
    