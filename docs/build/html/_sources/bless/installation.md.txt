# Installation and Usage

### Install Bless

Dependencies: `Python 3.10+`, `boolevard`, `mpi4py`, `pandas`, `numpy`, `multiprocessing`.

> 📝 **Note:** Bless is designed to run on high-performance computing (HPC) systems equipped with:
>
> * SLURM workload manager for job scheduling
> * An MPI implementation (e.g. OpenMPI or Intel MPI)
> * `Python 3.10+` and `mpi4py`

To install Bless, run the following command:

```
pip install git+https://github.com/farinasm/bless.git
```

### Quick Start

To execute Bless, a minimal invocation is:

```
bless --zips /path/to/zips --sampling 10 --mode synergies
```

Bless requires three mandatory parameters: `--zips`, `--sampling`, and  `--mode`. The `--zips` parameter specifies the directory containint the ZIP files with the expecter internal structure (see [*Helpers*](helpers.md)). The `--sampling` parameter defiens how many models are selected from the Gitsbe-generated ensemble (see [*Sampling*](sampling.md)). Finally, the `--mode` parameter controls the operational mode of Bless, which can be set to `synergies`, `countpaths`, or `full` (see [*Bless Modes*](blessmodes.md)).

Bless always operates using a configuration file (see [*Configuration*](configuration.md)). If no configuration file is explicitly provided via the optional `--config` parameter, Bless automatically falls back to a default configuration.

### Outputs

Bless produces outputs by augmenting the same ZIP files provided as input with an additional directory named Results. The specific contents of this directory depend on the selected operating mode (see [*Bless Modes*](blessmodes.md)):

- `synergies`: writes  `PathCounts` and `SynergyExcess` files .
- `countpaths`: writes a `PathCountsFull` file.
- `full`: writes  `PathCounts`, `PathCountsFull`, and `SynergyExcess` files.
