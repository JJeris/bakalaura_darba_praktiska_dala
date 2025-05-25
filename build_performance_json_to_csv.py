import json
import csv
import argparse
from pathlib import Path
from datetime import datetime

def find_step(steps, startswith_cmd):
    for step in steps:
        if step["cmd"].startswith(startswith_cmd):
            return step
    return None

def find_build_step(steps):
    for step in steps:
        cmd = step["cmd"]
        if cmd.startswith("npm run") and "install" not in cmd:
            return step
    return None

def compute_averages(rows, project_type):
    def safe_avg(key, divisor=1):
        values = [int(r[key]) for r in rows if r.get(key)]
        return round(sum(values) / len(values) / divisor, 2) if values else ""

    if project_type == "tauri":
        return {
            "file_name": "AVERAGES",
            "cargo_clean_duration_ms": safe_avg("cargo_clean_duration_ms"),
            "cargo_clean_duration_s": safe_avg("cargo_clean_duration_ms", divisor=1000),
            "npm_install_duration_ms": safe_avg("npm_install_duration_ms"),
            "npm_install_duration_s": safe_avg("npm_install_duration_ms", divisor=1000),
            "build_duration_ms": safe_avg("build_duration_ms"),
            "build_duration_s": safe_avg("build_duration_ms", divisor=1000),
            "msi_size_bytes": safe_avg("msi_size_bytes"),
            "exe_size_bytes": safe_avg("exe_size_bytes")
        }
    else: # elif project_type == "electronjs":
        return {
            "file_name": "AVERAGES",
            "npm_install_duration_ms": safe_avg("npm_install_duration_ms"),
            "npm_install_duration_s": safe_avg("npm_install_duration_ms", divisor=1000),
            "build_duration_ms": safe_avg("build_duration_ms"),
            "build_duration_s": safe_avg("build_duration_ms", divisor=1000),
            "msi_size_bytes": safe_avg("msi_size_bytes"),
            "exe_size_bytes": safe_avg("exe_size_bytes")
        }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_type", required=True)
    parser.add_argument("--input_dir", required=True)
    parser.add_argument("--output_csv", default="build_results_detailed.csv")
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    config_path = Path(args.config)
    output_csv = Path(args.output_csv)

    # Load test config
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    test_map = {test["result_file_name"]: test for test in config["tests"]}

    with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = []
        if args.project_type == "tauri":
            fieldnames = [
                "file_name", "iteration", "target_type",
                "system_cpu", "system_gpu", "system_os", "system_ram", "cpu_cores", "cpu_threads",
                "tauri", "node_version", "npm_version", "cargo_version", "rust_version", 
                "build_commands_used",
                "cargo_clean", "cargo_clean_start_ms", "cargo_clean_end_ms", "cargo_clean_duration_ms", "cargo_clean_duration_s",
                "delete_node_modules",
                "npm_install", "npm_install_start_ms", "npm_install_end_ms", "npm_install_duration_ms", "npm_install_duration_s",
                "build_start_ms", "build_end_ms", "build_duration_ms", "build_duration_s",
                "exe_size_bytes", "msi_size_bytes", 
            ]
        elif args.project_type == "electronjs":
            fieldnames = [
                "file_name", "iteration", "target_type",
                "system_cpu", "system_gpu", "system_os", "system_ram", "cpu_cores", "cpu_threads",
                "electron", "node_version", "npm_version",
                "build_commands_used",
                "delete_dist",
                "delete_node_modules",
                "npm_install", "npm_install_start_ms", "npm_install_end_ms", "npm_install_duration_ms", "npm_install_duration_s",
                "build_start_ms", "build_end_ms", "build_duration_ms", "build_duration_s",
                "exe_size_bytes", "msi_size_bytes", 
            ]

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for json_file in sorted(input_dir.glob("*.json")):
            if json_file.name not in test_map:
                print(f"Skipping unrecognized file: {json_file.name}")
                continue

            test_params = test_map[json_file.name]

            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    iterations = json.load(f)
            except Exception as e:
                print(f"Failed to read {json_file.name}: {e}")
                continue

            all_rows = []

            for iter_data in iterations:
                steps = iter_data["steps"]

                cargo_clean_step = find_step(steps, "cargo clean") # Tauri
                npm_install_step = find_step(steps, "npm install") # ElectronJS
                build_step = find_build_step(steps)
                
                row = {}
                if args.project_type == "tauri":
                    row = {
                        "file_name": json_file.name,
                        "iteration": iter_data["iteration"],
                        "target_type": test_params.get("target_type", ""),
                        "system_cpu": iter_data["system_info"].get("cpu", ""),
                        "system_gpu": iter_data["system_info"].get("gpu", ""),
                        "system_os": iter_data["system_info"].get("os", ""),
                        "system_ram": iter_data["system_info"].get("ram", ""),
                        "cpu_cores": iter_data["system_info"].get("cpu_cores", ""),
                        "cpu_threads": iter_data["system_info"].get("cpu_threads", ""),
                        "tauri": iter_data["framework_versions"].get("tauri", ""),
                        "node_version": iter_data["framework_versions"].get("node", ""),
                        "npm_version": iter_data["framework_versions"].get("npm", ""),
                        "cargo_version": iter_data["framework_versions"].get("cargo", ""),
                        "rust_version": iter_data["framework_versions"].get("rust", ""),
                        "build_commands_used": "; ".join([step["cmd"] for step in iter_data["steps"] if step["cmd"]]),
                        "cargo_clean": test_params.get("cargo_clean", False),
                        "cargo_clean_start_ms": cargo_clean_step["start_ms"] if cargo_clean_step else "",
                        "cargo_clean_end_ms": cargo_clean_step["end_ms"] if cargo_clean_step else "",
                        "cargo_clean_duration_ms": cargo_clean_step["duration_ms"] if cargo_clean_step else "",
                        "cargo_clean_duration_s": round(cargo_clean_step["duration_ms"] / 1000, 2) if cargo_clean_step else "",
                        "delete_node_modules": test_params.get("delete_node_modules", False),
                        "npm_install": test_params.get("npm_install", False),
                        "npm_install_start_ms": npm_install_step["start_ms"] if npm_install_step else "",
                        "npm_install_end_ms": npm_install_step["end_ms"] if npm_install_step else "",
                        "npm_install_duration_ms": npm_install_step["duration_ms"] if npm_install_step else "",
                        "npm_install_duration_s": round(npm_install_step["duration_ms"] / 1000, 2) if npm_install_step else "",
                        "build_start_ms": build_step["start_ms"] if build_step else "",
                        "build_end_ms": build_step["end_ms"] if build_step else "",
                        "build_duration_ms": build_step["duration_ms"] if build_step else "",
                        "build_duration_s": round(build_step["duration_ms"] / 1000, 2) if build_step else "",
                        "exe_size_bytes": iter_data.get("exe_size_bytes", ""),
                        "msi_size_bytes": iter_data.get("msi_size_bytes", ""),
                    }
                elif args.project_type == "electronjs":
                    row = {
                        "file_name": json_file.name,
                        "iteration": iter_data["iteration"],
                        "target_type": test_params.get("target_type", ""),
                        "system_cpu": iter_data["system_info"].get("cpu", ""),
                        "system_gpu": iter_data["system_info"].get("gpu", ""),
                        "system_os": iter_data["system_info"].get("os", ""),
                        "system_ram": iter_data["system_info"].get("ram", ""),
                        "cpu_cores": iter_data["system_info"].get("cpu_cores", ""),
                        "cpu_threads": iter_data["system_info"].get("cpu_threads", ""),
                        "electron": iter_data["framework_versions"].get("electron", ""),
                        "node_version": iter_data["framework_versions"].get("node", ""),
                        "npm_version": iter_data["framework_versions"].get("npm", ""),
                        "build_commands_used": "; ".join([step["cmd"] for step in iter_data["steps"] if step["cmd"]]),
                        "delete_dist": test_params.get("delete_dist", False),
                        "delete_node_modules": test_params.get("delete_node_modules", False),
                        "npm_install": test_params.get("npm_install", False),
                        "npm_install_start_ms": npm_install_step["start_ms"] if npm_install_step else "",
                        "npm_install_end_ms": npm_install_step["end_ms"] if npm_install_step else "",
                        "npm_install_duration_ms": npm_install_step["duration_ms"] if npm_install_step else "",
                        "npm_install_duration_s": round(npm_install_step["duration_ms"] / 1000, 2) if npm_install_step else "",
                        "build_start_ms": build_step["start_ms"] if build_step else "",
                        "build_end_ms": build_step["end_ms"] if build_step else "",
                        "build_duration_ms": build_step["duration_ms"] if build_step else "",
                        "build_duration_s": round(build_step["duration_ms"] / 1000, 2) if build_step else "",
                        "exe_size_bytes": iter_data.get("exe_size_bytes", ""),
                        "msi_size_bytes": iter_data.get("msi_size_bytes", ""),
                    }

                writer.writerow(row)
                all_rows.append(row)
                
            # Write average row
            avg_row = compute_averages(all_rows, args.project_type)
            writer.writerow(avg_row)
            writer.writerow({}) # Add empty row.
    print(f"\n Detailed CSV created at: {output_csv}")

if __name__ == "__main__":
    main()
