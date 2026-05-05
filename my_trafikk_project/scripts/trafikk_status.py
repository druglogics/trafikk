#!/usr/bin/env python3
"""
TRAFIKK Project Status Checker

Checks which pipeline steps have completed and suggests the next step.
No external dependencies (uses Python stdlib only).

Usage:
    python scripts/trafikk_status.py
"""

import os
from pathlib import Path
from collections import OrderedDict

# Define the runs directory relative to script location
PROJECT_ROOT = Path(__file__).parent.parent
RUNS_DIR = PROJECT_ROOT / "runs"
DATA_DIR = PROJECT_ROOT / "data"
LOGS_DIR = PROJECT_ROOT / "logs"

# Pipeline steps in order
PIPELINE = OrderedDict([
    ("01_celios", {
        "name": "Celios",
        "description": "Network calibration & omics integration",
        "check_files": ["*.csv"],  # Activity matrices
        "output_dir": RUNS_DIR / "01_celios",
    }),
    ("02_gitsbe", {
        "name": "Gitsbe",
        "description": "Boolean model ensemble generation",
        "check_files": ["*.zip"],  # Model ZIPs
        "output_dir": RUNS_DIR / "02_gitsbe",
    }),
    ("03_drexpa", {
        "name": "Drexpa",
        "description": "Drug panel & perturbation mapping",
        "check_files": ["drug_*.csv", "*/perturbations.txt"],  # Drug mappings or perturbations
        "output_dir": RUNS_DIR / "03_drexpa",
    }),
    ("04_oris", {
        "name": "Oris",
        "description": "Synergy scoring via signal propagation",
        "check_files": ["*/Results/SynergyExcess.txt", "*_results.zip"],  # Synergy results
        "output_dir": RUNS_DIR / "04_oris",
    }),
    ("05_synco", {
        "name": "Synco",
        "description": "Benchmarking against experimental data",
        "check_files": ["metrics.csv", "*.html"],  # Metrics or reports
        "output_dir": RUNS_DIR / "05_synco",
    }),
    ("06_siflex", {
        "name": "Siflex",
        "description": "Pathway analysis & interactive visualization",
        "check_files": ["*.html", "networks/*.html"],  # HTML dashboards
        "output_dir": RUNS_DIR / "06_siflex",
    }),
])


def check_raw_data():
    """Check if raw data exists."""
    raw_data_dir = DATA_DIR / "raw"
    if not raw_data_dir.exists():
        return False, 0

    files = list(raw_data_dir.rglob("*"))
    file_count = len([f for f in files if f.is_file()])
    return file_count > 0, file_count


def check_step(step_info):
    """Check if a pipeline step has completed."""
    output_dir = step_info["output_dir"]

    if not output_dir.exists():
        return False, 0

    file_count = 0
    found = False

    # Check for expected output files (using glob patterns)
    for pattern in step_info["check_files"]:
        matches = list(output_dir.glob(pattern))
        if matches:
            found = True
            file_count += len([m for m in matches if m.is_file()])

    return found, file_count


def print_status():
    """Print project status and next steps."""
    print("\n" + "=" * 60)
    print("TRAFIKK Project Status")
    print("=" * 60 + "\n")

    # Check raw data
    raw_ok, raw_count = check_raw_data()
    if raw_ok:
        print(f"[+] Raw data found ({raw_count} files)")
    else:
        print("[-] Raw data NOT found")
        print("    -> Add input files to data/raw/")

    # Check each pipeline step
    completed_steps = []
    pending_steps = []

    for step_id, step_info in PIPELINE.items():
        step_ok, file_count = check_step(step_info)
        step_name = step_info["name"]

        if step_ok:
            print(f"[+] {step_name}: Complete ({file_count} output files)")
            completed_steps.append(step_id)
        else:
            print(f"[ ] {step_name}: Pending")
            pending_steps.append(step_id)

    # Suggest next step
    print("\n" + "-" * 60)
    if pending_steps:
        next_step_id = pending_steps[0]
        next_step = PIPELINE[next_step_id]
        print(f">> Next step: {next_step['name']} ({next_step['description']})")

        # Print step-specific suggestion
        if next_step_id == "01_celios":
            print("   Command: celios config/celios.yaml")
        elif next_step_id == "02_gitsbe":
            print("   Command: gitsbe --config config/gitsbe.yaml")
            print("   Or (HPC): sbatch slurm/gitsbe_jobs/run_gitsbe_array.sh")
        elif next_step_id == "03_drexpa":
            print("   Command: drexpa --config config/drexpa.json")
        elif next_step_id == "04_oris":
            print("   Command: oris --config config/oris.toml --zips runs/02_gitsbe/*.zip")
            print("   Or (HPC): sbatch slurm/oris_jobs/run_oris.sh")
        elif next_step_id == "05_synco":
            print("   Command: synco --config config/synco.json")
        elif next_step_id == "06_siflex":
            print("   Command: siflex --config config/siflex.json")
    else:
        print(">> All pipeline steps completed!")
        print("   View results in: runs/06_siflex/")

    print("-" * 60 + "\n")


def main():
    """Main entry point."""
    # Verify project structure
    if not RUNS_DIR.exists():
        print(f"Error: runs/ directory not found at {RUNS_DIR}")
        print("Make sure you're running this from the project root.")
        exit(1)

    print_status()


if __name__ == "__main__":
    main()
