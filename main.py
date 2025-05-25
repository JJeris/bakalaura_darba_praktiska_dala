import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Defines tests subdivided into functions.
# Values are hardcoded to be easier to maintain.
def tauri_build(timestamp):
    base_dir = Path("results/tauri")
    config_path = Path("config/tauri/build-performance-variations-tauri.json")
    output_dir = base_dir / f"tauri_build_performance_{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)

    subprocess.run([
        "python",
        "build_performance.py",
        "--project_type", str("tauri"),
        "--config", str(config_path),
        "--output_dir", str(output_dir)
    ], check=True)

    subprocess.run([
        "python",
        "build_performance_json_to_csv.py",
        "--project_type", str("tauri"),
        "--input_dir", str(output_dir),
        "--output_csv", str(output_dir / "tauri_build_results.csv"),
        "--config", str(config_path)
    ], check=True)
    
    return 

def electronjs_build(timestamp):
    base_dir = Path("results/electronjs")
    config_path = Path("config/electronjs/build-performance-variations-electronjs.json")
    output_dir = base_dir / f"electronjs_build_performance_{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    subprocess.run([
        "python",
        "build_performance.py",
        "--project_type", str("electronjs"),
        "--config", str(config_path),
        "--output_dir", str(output_dir)
    ], check=True)

    subprocess.run([
        "python",
        "build_performance_json_to_csv.py",
        "--project_type", str("electronjs"),
        "--input_dir", str(output_dir),
        "--output_csv", str(output_dir / "electron_build_results.csv"),
        "--config", str(config_path)
    ], check=True)
    
    return

def tauri_runtime(timestamp):
    base_dir = Path("results/tauri")
    config_path = Path("config/tauri/runtime-performance-variations-tauri.json")
    output_dir = base_dir / f"tauri_runtime_performance_{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)

    subprocess.run([
        "python",
        "runtime_performance.py",
        "--project_type", str("tauri"),
        "--config", str(config_path),
        "--output_dir", str(output_dir)
    ], check=True)
    
    subprocess.run([
        "python",
        "runtime_performance_json_to_csv.py",
        "--project_type", str("tauri"),
        "--input_dir", str(output_dir),
        "--output_csv", str(output_dir / "tauri_runtime_results.csv"),
        "--config", str(config_path)
    ], check=True)

    return

def electronjs_runtime(timestamp):
    base_dir = Path("results/electronjs")
    config_path = Path("config/electronjs/runtime-performance-variations-electronjs.json")
    output_dir = base_dir / f"electronjs_runtime_performance_{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    subprocess.run([
        "python",
        "runtime_performance.py",
        "--project_type", str("electronjs"),
        "--config", str(config_path),
        "--output_dir", str(output_dir)
    ], check=True)

    subprocess.run([
        "python",
        "runtime_performance_json_to_csv.py",
        "--project_type", str("electronjs"),
        "--input_dir", str(output_dir),
        "--output_csv", str(output_dir / "electron_runtime_results.csv"),
        "--config", str(config_path)
    ], check=True)
    
    return

def tauri_startup(timestamp):
    base_dir = Path("results/tauri")
    config_path = Path("config/tauri/startup-performance-variations-tauri.json")
    output_dir = base_dir / f"tauri_startup_performance_{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)

    subprocess.run([
        "python",
        "startup_performance.py",
        "--project_type", str("tauri"),
        "--config", str(config_path),
        "--output_dir", str(output_dir)
    ], check=True)

    subprocess.run([
        "python",
        "startup_performance_json_to_csv.py",
        "--project_type", str("tauri"),
        "--input_dir", str(output_dir),
        "--output_csv", str(output_dir / "tauri_startup_results.csv"),
        "--config", str(config_path)
    ], check=True)

    return

def electronjs_startup(timestamp):
    base_dir = Path("results/electronjs")
    config_path = Path("config/electronjs/startup-performance-variations-electronjs.json")
    output_dir = base_dir / f"electronjs_startup_performance_{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)

    subprocess.run([
        "python",
        "startup_performance.py",
        "--project_type", str("electronjs"),
        "--config", str(config_path),
        "--output_dir", str(output_dir)
    ], check=True)

    subprocess.run([
        "python",
        "startup_performance_json_to_csv.py",
        "--project_type", str("electronjs"),
        "--input_dir", str(output_dir),
        "--output_csv", str(output_dir / "electron_startup_results.csv"),
        "--config", str(config_path)
    ], check=True)

    return

def main():
    """Executes tests and passes them their launch arguments."""
    
    if len(sys.argv) < 2:
        print("Script usage: python main.py <test_name>, like tauri_build, electronjs_build, tauri_runtime, electronjs_runtime, tauri_startup, electronjs_startup")
        return
    # Possible values: tauri_build, electronjs_build, tauri_runtime, electronjs_runtime, tauri_startup, electronjs_startup, all_...
    test_name = sys.argv[1].lower()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if test_name == "tauri_build":
        tauri_build(timestamp)

    elif test_name == "electronjs_build":
        electronjs_build(timestamp)

    elif test_name == "tauri_runtime":
       tauri_runtime(timestamp)

    elif test_name == "electronjs_runtime":
       electronjs_runtime(timestamp) 

    elif test_name == "tauri_startup":
        tauri_startup(timestamp)

    elif test_name == "electronjs_startup":
        electronjs_startup(timestamp)

    elif test_name == "all":
        tauri_build(timestamp)
        electronjs_build(timestamp)
        tauri_runtime(timestamp)
        electronjs_runtime(timestamp)
        tauri_startup(timestamp)
        electronjs_startup(timestamp)
        return
    
    elif test_name == "all_tauri":
        tauri_build(timestamp)
        tauri_runtime(timestamp)
        tauri_startup(timestamp)
        return
    
    elif test_name == "all_electronjs":
        electronjs_build(timestamp)
        electronjs_runtime(timestamp)
        electronjs_startup(timestamp)
        return
    
    else:
        print(f"Unrecognized test type: {test_name}")
        return

if __name__ == "__main__":
    main()
