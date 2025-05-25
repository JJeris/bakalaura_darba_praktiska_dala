import subprocess
import time
import psutil
import json
import argparse
from pathlib import Path
import platform
import os

ITERATIONS = 50

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
        print(f"Error identifying CPU model: {e}")
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
        print(f"Error identifying system info: {e}")
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
    
def monitor_startup_performance(exe_path, expected_main_process_count, cpu_threshold):
    """Launches the given .exe and waits for it to fully instance."""
    
    if not exe_path.exists():
        print(f"Error: Executable not found at {exe_path}")
        return {
            "success": False,
            "error": "Executable not found",
            "start_up_instance_moments": []
        }

    try:
        proc = subprocess.Popen([str(exe_path)])
        parent = psutil.Process(proc.pid)
        print(f"Launched {exe_path.name} with PID {proc.pid}")

        # Warm-up CPU counters for accurate immediate readings
        for p in [parent] + parent.children(recursive=True):
            try:
                p.cpu_percent(interval=None)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        start_ms = int(time.time() * 1000)
        start_up_instance_moments = []

        while True:
            iteration_start = time.time()

            if proc.poll() is not None:
                print("Process exited early during startup.")
                break

            try:
                all_procs = parent.children(recursive=True)
                all_procs.insert(0, parent)

                timestamp_ms = int(time.time() * 1000)

                total_cpu = 0.0
                main_process_count = 0

                for p in all_procs:
                    if not p.is_running():
                        continue
                    try:
                        cpu = p.cpu_percent(interval=None)
                        total_cpu += cpu
                        main_process_count += 1
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue

                # Log the current state
                start_up_instance_moments.append({
                    "timestamp_ms": timestamp_ms,
                    "main_pid": parent.pid,
                    "main_name": parent.name(),
                    "cpu_percent": total_cpu,
                    "main_process_count": main_process_count
                })

                print(f"[{timestamp_ms}] CPU: {total_cpu:.2f}% | Main procs: {main_process_count}")

                # Check if criteria are met
                if total_cpu < cpu_threshold and main_process_count >= expected_main_process_count:
                    print("Startup criteria met.")
                    break

            except psutil.NoSuchProcess:
                print("Main process ended.")
                break

            # Maintain consistent interval
            iteration_duration = time.time() - iteration_start
            time_to_sleep = max(0, 1.0 - iteration_duration)
            time.sleep(time_to_sleep)

        end_ms = int(time.time() * 1000)
        duration_ms = end_ms - start_ms

        # Cleanup
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
            "start_up_instance_moments": start_up_instance_moments
        }

    except Exception as e:
        print(f"Error during startup monitoring: {e}")
        return {
            "start_ms": int(time.time() * 1000),
            "end_ms": int(time.time() * 1000),
            "duration_ms": 0,
            "success": False,
            "error": str(e),
            "start_up_instance_moments": []
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
    print(test_cases)

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
                usage_result = {}
                if args.project_type == "tauri":
                    usage_result = monitor_startup_performance(build_file_path, 7, 1.0)
                elif args.project_type == "electronjs":
                    usage_result = monitor_startup_performance(build_file_path, 4, 1.0)
                iteration["startup_instances"] = usage_result
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
    