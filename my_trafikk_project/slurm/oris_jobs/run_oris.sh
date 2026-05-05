#!/bin/bash
#SBATCH --job-name=oris_synergy
#SBATCH --partition=CPUQ                # Change to your partition/queue
#SBATCH --account=myuser                # Change to your account
#SBATCH --time=24:00:00                 # Wall-time limit

#SBATCH --nodes=4
#SBATCH --ntasks-per-node=14            # MPI tasks per node
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=2GB

#SBATCH --output=logs/oris_%j.out
#SBATCH --error=logs/oris_%j.err

# ==========================================
# Oris Synergy Scoring with MPI
# ==========================================
# This script runs Oris across multiple HPC nodes using MPI for synergy scoring.
# Oris is computationally intensive; MPI parallelization is recommended.

# Load environment (match config/oris.toml preamble)
module load intel/2024a
module load SciPy-bundle/2024.05-gfbf-2024a
module load Python/3.12.3-GCCcore-13.3.0

# Verify MPI setup
echo "=========================================="
echo "Oris Synergy Scoring (MPI)"
echo "=========================================="
echo "Nodes: $SLURM_NNODES"
echo "Tasks per node: $SLURM_NTASKS_PER_NODE"
echo "Total tasks: $SLURM_NTASKS"
echo "=========================================="

# Run Oris with config and MPI
# Replace --zips with your actual model ZIP files
mpirun -np $SLURM_NTASKS oris \
  --config config/oris.toml \
  --zips runs/02_gitsbe/*.zip \
  --mode synergies \
  --sampling 50 \
  --perturbation-dir runs/03_drexpa \
  --verbose

# Check exit status
if [ $? -eq 0 ]; then
    echo "✓ Oris completed successfully"
else
    echo "✗ Oris failed (exit code: $?)"
    exit 1
fi

echo "Results saved to: runs/04_oris/"
echo "Next step: Run Synco for benchmarking"
