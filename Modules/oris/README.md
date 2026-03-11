# Oris

**Oris** — *Boolean Logic-Based Estimation of Synergy Scores* — is a module built on top of [BooLEVARD](https://github.com/farinasm/boolevard) for computing Bliss-type synergy scores from Boolean model ensembles produced with [Gitsbe](https://github.com/druglogics/gitsbe). Within [Trafikk](https://github.com/druglogics/trafikk), Oris operates on Celios-calibrated model ensembles to assess the impact of single and combined perturbations defined with Drexpa.

In addition to synergy scoring, Oris can also be used as a generic path-based signal transduction quantifier: it measures the propagation of activity from input nodes to selected output nodes in Boolean models, which can serve as a proxy for cell viability or functional output.

---

## Features

- **Synergy Mode** (`--mode synergies`): computes Bliss synergy excess for drug pair perturbations.
- **Count Paths Mode** (`--mode countpaths`): quantifies signal propagation toward all Boolean nodes.
- **Full Mode** (`--mode full`): runs both synergy and count-paths analyses in a single execution.

---

## Requirements

- `Python 3.10+`
- [BooLEVARD](https://github.com/farinasm/boolevard)
- `mpi4py`
- `pandas`
- `numpy`

> **Note:** Oris is designed to run on high-performance computing (HPC) systems equipped with:
>
> - SLURM workload manager for job scheduling
> - An MPI implementation (e.g. OpenMPI or Intel MPI)

---

## Installation

```bash
pip install git+https://github.com/druglogics/trafikk.git#subdirectory=Modules/oris
```

---

## Quick Start

```bash
oris --zips /path/to/zips --sampling 10 --mode synergies
```

Oris requires three mandatory parameters:

| Parameter     | Description                                                                 |
| ------------- | --------------------------------------------------------------------------- |
| `--zips`      | Path to the directory containing input ZIP files                            |
| `--sampling`  | Number of models to sample from the Gitsbe-generated ensemble              |
| `--mode`      | Operational mode: `synergies`, `countpaths`, or `full`                      |

Optional parameters include `--config` (custom TOML configuration file), `--skip-initial` (skip media and initial conditions), `--timeout-sampling`, `--timeout-paths`, `--dry-run`, and `--verbose`.

---

## Configuration

Oris uses a TOML configuration file to control its execution environment, HPC scheduling, and simulation parameters. If no file is provided via `--config`, Oris falls back to a built-in default.

The configuration file has three sections:

1. **[slurm]** — HPC scheduling directives
2. **[env]** — Software environment setup
3. **[oris]** — Simulation parameters

Example:

```toml
[slurm]
partition       = "CPUQ"
nodes           = 18
ntasks_per_node = 14
time            = "24:00:00"
auto_submit     = true

[env]
preamble = """
module load intel/2024a
module load Python/3.12.3-GCCcore-13.3.0
"""

[oris]
default_sampling = 10
media_targets    = ["EGFR", "IGF1R", "MET"]
timeout_sampling = 300
timeout_paths    = 600
```

---

## Outputs

Oris augments the input ZIP files with a `Results/` directory containing:

| Mode         | Output files                                          |
| ------------ | ----------------------------------------------------- |
| `synergies`  | `PathCounts`, `SynergyExcess`                         |
| `countpaths` | `PathCountsFull`                                      |
| `full`       | `PathCounts`, `PathCountsFull`, `SynergyExcess`       |

---

## License

This project is licensed under the GNU General Public License v3.0. See [LICENSE](LICENSE) for details.
