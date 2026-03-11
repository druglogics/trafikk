# Configuration

Oris uses a TOML configuration file to control its **execution environment**, **HPC scheduling**, and **simulation parameters**. Oris will use the configuration file specified via the optional `--config` argument. If no file is provided, Oris falls back to an internal default configuration.

The configuration file is organized into three sections:

1. **[slurm]** - HPC scheduling directives (SLURM-specific)
2. **[env]** - Software environment setup
3. **[oris]** - Oris-specific simulation parameters

Below is the default configuration used by Oris:

```
# ==========================================
# ORIS - CLUSTER CONFIGURATION / PIPELINE
# ==========================================

# 🖥️ CLUSTER (Slurm)
[slurm]
partition           = "CPUQ"          # Cluster queue
account             = "myuser"      # Project (if applies)
time                = "24:00:00"      # Time limit ⏳

nodes               = 18              # Number of nodes 🧩
ntasks_per_node     = 14              # MPI tasks per node 🚀

output              = "oris_%j.out"  # Standard log 📄
error               = "oris_%j.err"  # Error log ❗
auto_submit         = true            # Automatic sbatch launch 🧚

# 🧬 ENVIRONMENT
[env]
preamble = """
module load intel/2024a
module load SciPy-bundle/2024.05-gfbf-2024a
module load Python/3.12.3-GCCcore-13.3.0
"""

# 🧠 ORIS configuration
[oris]
default_sampling     = 10                       # When no --sampling 🧮
media_targets        = ["EGFR", "IGF1R", "MET"] # Media nodes 🌐
timeout_sampling     = 300                      # Sampling threshold (seconds) ⏱️
timeout_paths        = 600                      # CountPaths threshold (seconds) ⏱️
```

### 🖥️ [slurm] - HPC Scheduling Section

This section controls how Oris interacts with **SLURM** when submitting jobs.

| Parameter           | Type   | Description                                     |
| ------------------- | ------ | ----------------------------------------------- |
| `partition`       | string | SLURM partition/queue to submit jobs to         |
| `account`         | string | Project/account for billing (cluster-dependent) |
| `time`            | string | Wall-time limit in `HH:MM:SS` format          |
| `nodes`           | int    | Number of SLURM nodes requested                 |
| `ntasks_per_node` | int    | MPI tasks spawned per node                      |
| `output`          | string | Path for standard output logs (`%j` = JobID)  |
| `error`           | string | Path for error logs                             |
| `auto_submit`     | bool   | If `true`, Oris submits via `sbatch`       |

> 📝 If `auto_submit = false`, Oris witll instead generate the `.sbatch` script and print instructions for manual submission.

### 🧬 [env] - Software Environment Section

This section defines the **runtime software environment**, typically using `module load`, `conda activate`, or similar commands.

| Parameter    | Type             | Description                                  |
| ------------ | ---------------- | -------------------------------------------- |
| `preamble` | multiline string | Shell commands executed before job execution |

Common uses include:

- loading compiler toolchains
- activating conda environments
- loading MPI implementations
- loading Python modules

### 🧠 [oris] - Simulation Parameters Section

This section controls Oris-specific runtime behavior:

| Parameter            | Type          | Description                                                        |
| -------------------- | ------------- | ------------------------------------------------------------------ |
| `default_sampling` | int           | Default number of sampled models if `--sampling` is not provided |
| `media_targets`    | array[string] | Input/media nodes forced ON during initial condition filtering     |
| `timeout_sampling` | int (seconds) | Max time for `CountPaths` during model sampling                  |
| `timeout_paths`    | int (seconds) | Max time for `CountPaths` during full simulation                 |

> 📝 **Notes:**
>
> - `media_targets` defines **culture medium context**, enforcing media nodes as inputs during initial condition selection.
> - `timeout_sampling` applies only to **sampling mode**, i.e. selecting fast-running models.
> - `timeout_paths` applies to **CountPaths runs** under all modes.

### 💡 **Example Usage**

To run Oris with a custom configuration:

`oris --zips /path/to/zips --mode full --sampling 20 --config /path/to/oris_config.toml`

If `--config` is omitted, Oris will load its internal default.

> 📝 Depending on your HPC system you may need to modify:
>
> - `partition`
> - `account`
> - `module load` lines
> - MPI versions
> - Python versions (always 3.10+)
>
> Oris does **not** validate environment modules, so incorrect module names will result in SLURM job failures at runtime.
