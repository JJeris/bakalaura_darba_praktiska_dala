import json
import csv
import argparse
from pathlib import Path

def compute_averages(rows):
    def safe_avg(key):
        values = [float(r[key]) for r in rows if r.get(key)]
        return round(sum(values) / len(values), 2) if values else ""

    return {
        "file_name": "AVERAGES",
        "process_count": safe_avg("process_count"),
        "duration_ms": safe_avg("duration_ms"),
        "duration_s": safe_avg("duration_s"),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_type", required=True)
    parser.add_argument("--input_dir", required=True)
    parser.add_argument("--output_csv", default="runtime_results_detailed.csv")
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    config_path = Path(args.config)
    output_csv = Path(args.output_csv)

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    test_map = {test["result_file_name"]: test for test in config["tests"]}

    with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
        if args.project_type == "tauri":
            fieldnames = [
                "file_name", "iteration", "timestamp_ms", "main_pid", "main_name",
                "executable_type", "system_os", "system_cpu", "system_gpu", "system_ram",
                "cpu_cores", "cpu_threads",
                "node_version", "npm_version", "cargo_version", "rust_version",
                "build_commands_used",
                "start_ms", "end_ms", "duration_ms", "duration_s", "success",
                "process_count",
            ]
        elif args.project_type == "electronjs":
            fieldnames = [
                "file_name", "iteration", "timestamp_ms", "main_pid", "main_name",
                "executable_type", "system_os", "system_cpu", "system_gpu", "system_ram",
                "cpu_cores", "cpu_threads",
                "node_version", "npm_version",
                "build_commands_used",
                "start_ms", "end_ms", "duration_ms", "duration_s", "success",
                "process_count",
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
                startup = iter_data.get("startup_instances")
                if not startup or not startup.get("start_up_instance_moments"):
                    continue

                instance = startup["start_up_instance_moments"][-1]
                row = {}
                if args.project_type == "tauri":
                    row = {
                        "file_name": json_file.name,
                        "iteration": iter_data.get("iteration", ""),
                        "timestamp_ms": instance.get("end_ms", ""),
                        "main_pid": instance.get("main_pid", ""),
                        "main_name": instance.get("main_name", ""),
                        "executable_type": test_params.get("executable_type", ""),
                        "system_os": iter_data["system_info"].get("os", ""),
                        "system_cpu": iter_data["system_info"].get("cpu", ""),
                        "system_gpu": iter_data["system_info"].get("gpu", ""),
                        "system_ram": iter_data["system_info"].get("ram", ""),
                        "cpu_cores": iter_data["system_info"].get("cpu_cores", ""),
                        "cpu_threads": iter_data["system_info"].get("cpu_threads", ""),
                        "node_version": iter_data["framework_versions"].get("node", ""),
                        "npm_version": iter_data["framework_versions"].get("npm", ""),
                        "cargo_version": iter_data["framework_versions"].get("cargo", ""),
                        "rust_version": iter_data["framework_versions"].get("rust", ""),
                        "build_commands_used": "; ".join(iter_data.get("build_commands_used", [])),
                        "start_ms": startup.get("start_ms", ""),
                        "end_ms": startup.get("end_ms", ""),
                        "duration_ms": startup.get("duration_ms", ""),
                        "duration_s": round(startup.get("duration_ms", 0) / 1000, 2),
                        "success": startup.get("success", ""),
                        "process_count": instance.get("process_count", "")
                    }
                elif args.project_type == "electronjs":
                    row = {
                        "file_name": json_file.name,
                        "iteration": iter_data.get("iteration", ""),
                        "timestamp_ms": instance.get("end_ms", ""),
                        "main_pid": instance.get("main_pid", ""),
                        "main_name": instance.get("main_name", ""),
                        "executable_type": test_params.get("executable_type", ""),
                        "system_os": iter_data["system_info"].get("os", ""),
                        "system_cpu": iter_data["system_info"].get("cpu", ""),
                        "system_gpu": iter_data["system_info"].get("gpu", ""),
                        "system_ram": iter_data["system_info"].get("ram", ""),
                        "cpu_cores": iter_data["system_info"].get("cpu_cores", ""),
                        "cpu_threads": iter_data["system_info"].get("cpu_threads", ""),
                        "node_version": iter_data["framework_versions"].get("node", ""),
                        "npm_version": iter_data["framework_versions"].get("npm", ""),
                        "build_commands_used": "; ".join(iter_data.get("build_commands_used", [])),
                        "start_ms": startup.get("start_ms", ""),
                        "end_ms": startup.get("end_ms", ""),
                        "duration_ms": startup.get("duration_ms", ""),
                        "duration_s": round(startup.get("duration_ms", 0) / 1000, 2),
                        "success": startup.get("success", ""),
                        "process_count": instance.get("process_count", "")
                    }
                
                writer.writerow(row)
                all_rows.append(row)

            if all_rows:
                avg_row = compute_averages(all_rows)
                writer.writerow(avg_row)
                writer.writerow({})  # Empty line

    print(f"\nStartup performance CSV created at: {output_csv}")


if __name__ == "__main__":
    main()
