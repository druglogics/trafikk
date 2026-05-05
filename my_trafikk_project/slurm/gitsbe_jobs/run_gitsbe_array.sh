#!/bin/bash
#SBATCH --job-name=gitsbe_array
#SBATCH --partition=CPUQ                # Change to your partition/queue
#SBATCH --account=myuser                # Change to your account
#SBATCH --time=12:00:00                 # Wall-time limit
#SBATCH --nodes=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32GB

#SBATCH --output=logs/gitsbe_%j.out
#SBATCH --error=logs/gitsbe_%j.err
#SBATCH --array=1-2                     # Number of cell lines (adjust as needed)

# ==========================================
# Gitsbe Array Job for Multiple Cell Lines
# ==========================================
# This script runs Gitsbe for multiple cell lines in parallel using SLURM arrays.
# Each cell line is processed by one task.

# Load environment
module load intel/2024a
module load Java/17.0.6
module load Maven/3.8.6

# Define cell lines
CELLLINES=("CellLine_1" "CellLine_2" "CellLine_3")

# Get current cell line
CELLLINE=${CELLLINES[$SLURM_ARRAY_TASK_ID - 1]}

echo "=========================================="
echo "Running Gitsbe for: $CELLLINE"
echo "Task: $SLURM_ARRAY_TASK_ID / $SLURM_ARRAY_TASK_MAX"
echo "=========================================="

# Run Gitsbe (replace with actual Gitsbe command for your setup)
# This is a placeholder; adjust command based on how Gitsbe is installed
gitsbe \
  --config config/gitsbe.yaml \
  --cell-line "$CELLLINE" \
  --input "runs/01_celios/cell_lines/${CELLLINE}.csv" \
  --output "runs/02_gitsbe/${CELLLINE}_models.zip" \
  --verbose

# Check exit status
if [ $? -eq 0 ]; then
    echo "✓ Gitsbe completed for $CELLLINE"
else
    echo "✗ Gitsbe failed for $CELLLINE (exit code: $?)"
    exit 1
fi

echo "Done."
