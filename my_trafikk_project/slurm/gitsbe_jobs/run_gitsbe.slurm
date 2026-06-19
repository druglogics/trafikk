#!/bin/bash
#SBATCH --job-name=gitsbe_phenotypes  # Name of the job
#SBATCH --output=output_%A_%a.out       # Output file
#SBATCH --error=error_%A_%a.err         # Error file
#SBATCH --array=0                    # Array range (adjust based on your directories)
#SBATCH --cpus-per-task=8               # Number of cores per job
#SBATCH --mem=5G                        # Memory per job
#SBATCH --time=00:60:00                 # Time limit for each job
#SBATCH --partition=CPUQ             # Partition to submit to

module load  Java/11.0.20

# Dynamically get all subdirectories
directories=($(ls -d */ | sed 's:/$::'))

# Determine the directory for this job
cell_line=${directories[$SLURM_ARRAY_TASK_ID]}

# Define the file paths dynamically for the current subdirectory
network_file="${cell_line}/network.sif"
trainingdata_file="${cell_line}/${cell_line}_training"
config_file="${cell_line}/config"
modeloutputs_file="${cell_line}/modeloutputs"

# Print debugging information
echo "Detected cell line directory: $cell_line"
echo "Checking files:"
echo "Network: $network_file (exists: $(test -f "$network_file" && echo yes || echo no))"
echo "Training data: $trainingdata_file (exists: $(test -f "$trainingdata_file" && echo yes || echo no))"
echo "Config: $config_file (exists: $(test -f "$config_file" && echo yes || echo no))"
echo "Modeloutputs: $modeloutputs_file (exists: $(test -f "$modeloutputs_file" && echo yes || echo no))"

# Check if required files exist
if [[ -f "$network_file" && -f "$trainingdata_file" && -f "$config_file" && -f "$modeloutputs_file" ]]; then
    # Run the Java command with specified options
    echo "Directory: $cell_line"
    java -cp gitsbe-1.3.1-jar-with-dependencies.jar eu.druglogics.gitsbe.Launcher \
        --network=$network_file \
        --trainingdata=$trainingdata_file \
        --config=$config_file \
        --modeloutputs=$modeloutputs_file
else
    echo "Missing required files in $cell_line" >&2
fi