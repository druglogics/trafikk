# TRAFIKK Project Template

A structured, step-by-step guide for running the complete TRAFIKK pipeline on your data.

## What is This?

**TRAFIKK** predicts which combinations of cancer drugs will work well together and explains *why* they're synergistic at the molecular level.

**This template** provides a ready-made project structure so you don't have to set up folders and configurations from scratch. It guides you through each pipeline stage with pre-made config files, clear data input/output locations, and HPC job templates.

**In short:** If you have cancer cell line data (gene expression, mutations, etc.), a Boolean model, and a drug list, TRAFIKK can predict drug synergies. This template makes it easy.

---

## Is This For You?

**Use this template if you have:**

- [ ] Cancer cell line data (expression, mutations, CNV, TF activity)
- [ ] A Boolean network file (SIF format, e.g., from your lab or curated databases)
- [ ] A list of drugs you want to test
- [ ] (Optional) Experimental synergy data to benchmark against

**You can skip this template if you:**

- Only want to predict drug effects (you can use the DrugLogics pipeline)
- Don't have a network file (you'd need to create one first — outside scope of TRAFIKK)
We recommend using already built models, build new throught manual curation, or using automatic pipelines, such as NeKo. 
- Want to use TRAFIKK modules independently (install them directly)

---

## How It Works (60-Second Overview)

```
Your Data
   ↓
[1] Celios: Calibrate network to your cell lines (using omics data)
   ↓
[2] Drexpa: Map drugs to network nodes and create drug panel + perturbations
   ↓
[3] Gitsbe: Generate diverse models for each cell line
   ↓
[4] Oris: Predict synergy scores for all drug pairs + global signal propagation
   ↓
[5] Synco: Compare predictions vs. experimental data (optional)
   ↓
[6] Siflex: Explore why synergies work (pathway and network analysis)
   ↓
Interactive Results + Mechanistic Insights
```

Each step outputs files that feed into the next. This template keeps everything organized.

---

## Overview

This project template guides you through all 6 stages of the TRAFIKK pipeline:

```
Celios ➜ Drexpa ➜ Gitsbe ➜ Oris ➜ Synco ➜ Siflex
 Omics    Drugs    Models   Synergy  Bench  Analysis
```

Each step is **run independently** with its own configuration file and output folder. You can run all steps sequentially or skip to specific stages.

**Key principle:** Outputs from one step become inputs to the next. This template makes those connections explicit.

---

## Directory Structure

```
my_trafikk_project/
├── config/              # Configuration files for each step
├── data/raw/            # Your input data (networks, omics, drugs, etc.)
├── runs/                # Pipeline outputs organized by step
│   ├── 01_celios/       # Activity matrices
│   ├── 02_drexpa/       # Drug panels & perturbation profiles
│   ├── 03_gitsbe/       # Boolean model ensembles
│   ├── 04_oris/         # Synergy scores
│   ├── 05_synco/        # Benchmarking metrics
│   └── 06_siflex/       # Interactive visualizations
├── slurm/               # SLURM job submission scripts (for HPC)
├── logs/                # SLURM and pipeline logs
├── reports/             # Final figures and summaries
└── scripts/trafikk_status.py  # Status checker
```

---

## Quick Start

### 0. Prerequisites

**Required:**
- Python 3.9+ with `pip` — Most steps use Python modules
- Java 11+ — Gitsbe (step 2) runs as Java
- ~50 GB disk space — Pipeline generates large model files

**Optional (for HPC clusters):**
- SLURM — Only if running on a cluster. Local (single-machine) runs don't need this
- Gitsbe JAR file — Already included in `slurm/gitsbe_jobs/gitsbe-1.3.1-jar-with-dependencies.jar`

**Check what you have:**

```bash
# Python
python --version           # Should be 3.9+

# Java
java -version             # Should be 11+

# SLURM (if on HPC cluster)
which sbatch              # If installed, you can use HPC mode
```

**Install Python dependencies:**
```bash
pip install -r requirements.txt
```

This installs: `celios`, `drexpa`, `oris`, `synco`, `siflex` at the pinned versions (see `requirements.txt`).

### 1. Set Up Your Workspace

**Option A: Copy this template (Recommended for new projects)**

Use this if you want to start a new TRAFIKK analysis:

```bash
# Copy the template to your workspace
cp -r my_trafikk_project ~/my_breast_cancer_project
cd ~/my_breast_cancer_project

# Create a Python virtual environment (one per project)
python -m venv venv
source venv/bin/activate              # On Mac/Linux
# OR
.\venv\Scripts\activate               # On Windows

# Install TRAFIKK modules
pip install -r requirements.txt
```

This gives you:
- ✓ Pre-organized folder structure
- ✓ Config templates for all 6 steps
- ✓ SLURM job scripts
- ✓ Status checker script

**Option B: Clone TRAFIKK repo (if developing or contributing)**

Use this if you're working on TRAFIKK itself:

```bash
git clone https://github.com/druglogics/trafikk.git
cd trafikk
python -m venv venv
source venv/bin/activate
pip install -e .
```

---

**Virtual Environment: One Per Project or Global?**

**Recommended: One venv per project**

Each project folder has its own isolated environment:

```bash
~/projects/
├── breast_cancer_synergy/
│   ├── venv/                         # Project 1's environment
│   ├── config/
│   ├── data/
│   └── runs/
├── lung_cancer_synergy/
│   ├── venv/                         # Project 2's environment
│   ├── config/
│   ├── data/
│   └── runs/
```

**Pros:** Easy to share projects, no version conflicts, reproducible setup

**On HPC clusters:** Ask your admin, but typically use shared modules instead:

```bash
module load Python/3.11.3
pip install --user -r requirements.txt
```

---

**Quick Verification After Setup**

```bash
# Run from project root
python scripts/trafikk_status.py       # Should show all steps as Pending

java -version                           # Should show Java 11+

pip show celios drexpa oris            # Should show installed versions
```

### 2. Prepare Your Raw Data

Place input files in `data/raw/`:

```
data/raw/
├── networks/
│   └── your_network.sif         # Boolean network
├── omics/
│   ├── expression.csv           # Gene expression (TPM, log2, etc.)
│   ├── mutations.csv            # Binary mutation matrix
│   ├── cnv.csv                  # Copy number variation matrix
│   └── tf_activity.csv          # TF activity scores
├── drugs/
│   ├── drug_names.txt           # One drug name per line
│   ├── drug_targets.csv         # Drug → gene targets mapping
│   ├── synergy_data.csv         # Experimental synergy data (optional)
│   └── tissue_cellline_map.csv  # Tissue → cell lines mapping
├── hgnc/
│   ├── hgnc_complete_set.txt    # HGNC gene symbol reference
│   └── manual_symbols.csv       # Manual gene → symbol mappings (optional)
└── metadata/
    └── cell_line_list.csv       # Cell line metadata
```

### 3. Edit Configuration Files

Each step has a configuration file in `config/`:

- `project.yaml` — Project metadata
- `celios.yaml` — Step 1: Network calibration
- `gitsbe.yaml` — Step 2: Model generation
- `drexpa.json` — Step 3: Drug mapping
- `oris.toml` — Step 4: Synergy scoring (with SLURM settings)
- `synco.json` — Step 5: Benchmarking
- `siflex.json` — Step 6: Visualization

Edit each config with your file paths and parameters. **Templates are provided with placeholders.**

---

## New User Quick Ref

**I just got this template. What do I do first?**
1. Copy the template: `cp -r my_trafikk_project ~/my_project`
2. Set up venv: `python -m venv venv && source venv/bin/activate`
3. Install packages: `pip install -r requirements.txt`
4. Read "3. Prepare Your Raw Data" to understand what files you need
5. Follow "4. Run Each Step" step-by-step

**I have no data yet. Can I still test this?**
- Yes! Ask your lab for sample data or find public CCLE/GDSC data
- Download a pre-made network file (SIF format)
- The template structure works the same way

**Should I use one venv or multiple?**
- One venv per project (recommended)
- Makes projects portable and shareable
- Each project is in its own folder with its own `venv/`

**Can I skip steps?**
- Yes. Celios → Gitsbe are mandatory
- Drexpa, Oris, Synco, Siflex are optional
- See "Running Specific Steps" section below

**Do I need HPC?**
- No, but helpful. Oris is slow on laptops
- Celios + Gitsbe can run locally (8GB RAM, takes hours)
- See "Run on HPC" section

**Where do I put my data?**
- `data/raw/` folder (exact structure in "3. Prepare Your Raw Data")

---

## Sample Data

This template includes **real CCLE (Cancer Cell Line Encyclopedia) sample data** ready to test the pipeline without needing your own data.

**Included sample files** in `data/raw/omics/`:
- `rnaseq_tpm_20220624.csv` (246 MB) — Gene expression data from ~1,000 CCLE cell lines
- `CCLE_muts_binary.csv` (2.2 MB) — Binary mutation matrix
- `CCLE_CNV_binary.csv` (22 MB) — Copy number variation matrix
- `ccle_tf_activities.csv` (58 MB) — Transcription factor activity scores

**What's missing (you need to provide):**
- Network file (e.g., `data/raw/networks/your_network.sif`)
- Cell line list (e.g., `data/raw/metadata/cell_line_list.csv`)
- Celios config pointing to the network and these files

**Try Celios with sample data:**

```bash
# 1. Activate your venv
source venv/bin/activate

# 2. Get a network file (e.g., from your lab or a database)
# For demo: use any SIF file or create a minimal one

# 3. Create a cell line list (CSV with one cell line per row)
echo "MCF7,T47D,HCT116" > data/raw/metadata/cell_line_list.csv

# 4. Edit config/celios.yaml:
#    - Point to your network: data/raw/networks/your_network.sif
#    - Activity file already points to rnaseq_tpm_20220624.csv
#    - Mutations, CNV, TF already configured

# 5. Run Celios
celios config/celios.yaml

# 6. Check results
python scripts/trafikk_status.py  # Should show Celios: Complete
```

---

## Pipeline Steps (In Order)

### Step 1: Celios — Network Calibration

**Purpose:** Integrate omics data and calibrate the Boolean network to your cell lines.

**Inputs:**
- SIF network file (`data/raw/networks/your_network.sif`)
- Omics data: expression, mutations, CNV, TF activity (`data/raw/omics/`)
- HGNC gene symbol reference (`data/raw/hgnc/hgnc_complete_set.txt`)
- Cell line list (`data/raw/metadata/cell_line_list.csv`)

**Config file:** `config/celios.yaml`

**Run:**
```bash
celios config/celios.yaml
```

**Expected outputs** in `runs/01_celios/`:
- `activity_master_matrix/` — All omics data sources per cell line
- `activity_from_master/` — Omics data per cell line following data source priority
- `node_HGNC_dict.csv` — Gene → node mappings
- `identifiers.csv` — Cell line identifiers (SIDM, CVCL, RRID, ACH)
- Logs: `run_log.txt`
- `cell_lines/` — Cell line folders with per-cell-Line calibration files, compatible with gitsbe
- `tissue_folders/` — Tissue-organized output (if configured)

**What's next:** Outputs feed into Gitsbe as calibrated activity profiles.

---
### Step 2: Drexpa — Drug Panel & Perturbation Mapping

**Purpose:** Map drugs to network nodes and generate perturbation profiles.

**Inputs:**
- Gitsbe output: ZIPs from `runs/02_gitsbe/`
- Drug names file: `data/raw/drugs/drug_names.txt`
- (Optional) Experimental synergy data: `data/raw/drugs/experimental_synergies.csv`
- Node dictionary: from Celios (`runs/01_celios/node_HGNC_dictionary.csv`)
- (OPtional) Tissue-cellline mapping: `data/raw/metadata/tissue_cline_map.csv`

**Config file:** `config/drexpa.json`

**Run:**
```bash
drexpa --config config/drexpa.json
```

**Expected outputs** in `runs/03_drexpa/`:
- `drug_ChEMBL_IDs.csv` — Drug → ChEMBL ID mapping
- `drug_node_targets.csv` — Drug → node targets
- `drug_panel_df.csv` — Summary of all drugs
- `{Cell_line}/perturbations` — Per-cell-line perturbation profiles
- `{Cell_line}/observed_synergies` — Per-cell-line synergy data (if provided)
- Logs: `drexpa.log`

**What's next:** Perturbation files are inputs to Oris.
### Step 3: Gitsbe — Boolean Model Ensemble Generation

**Purpose:** Generate a diverse ensemble of Boolean models for each cell line using genetic algorithm optimization.

**Input structure:**

Gitsbe expects each cell line in its own directory with 6 required files/folders:

```
runs/03_gitsbe/
├── CellLine_1/
│   ├── network.sif         ← Network file
│   ├── CellLine_1_training        ← Training data file
│   ├── drugpanel                  ← List of drug IDs and node targets file
│   ├── config                     ← Configuration file
│   ├── perturbations              ← List of single and double perturbations file
│   └── modeloutputs               ← Defined model outputs as phenotype-proxies
├── CellLine_2/
│   ├── network.sif
│   ├── CellLine_2_training
│   ├── drugpanel
│   ├── config
│   ├── perturbations
│   └── modeloutputs
└── ...
```

**Prepare your inputs:**

```bash
# Create directory structure from Celios and Drexpa outputs
mkdir -p runs/03_gitsbe/cell_line_runs

# Place input files for each cell line
# (network, training data, config from runs/01_celios/ or data/raw/)
cp runs/01_celios/CellLine_1_training runs/02_gitsbe/CellLine_1/
cp your_network.sif runs/02_gitsbe/CellLine_1/network.sif
cp gitsbe_config runs/02_gitsbe/CellLine_1/config
```

**Run (local, single cell line):**

```bash
cd runs/02_gitsbe/CellLine_1
java -cp ../../slurm/gitsbe_jobs/gitsbe-1.3.1-jar-with-dependencies.jar \
  eu.druglogics.gitsbe.Launcher \
  --network=network.sif \
  --trainingdata=CellLine_1_training \
  --config=config \
  --modeloutputs=modeloutputs
```

**Run (HPC with SLURM, multiple cell lines):**

```bash
# Adjust --array to match number of cell line directories
sbatch --array=0-1 run_gitsbe.slurm
```

Script will automatically detect all subdirectories in `runs/02_gitsbe/` and run Gitsbe for each.

**Expected outputs** in `runs/02_gitsbe/cell_line_runs`:


**What's next:** Model outputs are used by Oris.

---

### Step 4: Oris — Synergy Scoring via Signal Propagation

**Purpose:** Run Boolean model simulations using BooLEVARD to compute signal propagation and, optionally, Bliss synergy scores for drug perturbations.

Oris is designed to run on HPC systems using SLURM and MPI. It takes prepared ZIP files from the previous TRAFIKK steps and writes the results back into those same ZIP files by adding a `Results/` directory.

**Inputs:**

Oris expects a directory containing one or more ZIP files. Each ZIP file should contain the required internal TRAFIKK structure:

```text
src/
├── Models/              # Gitsbe-generated Boolean model ensemble
├── training/            # Calibration/training data
├── perturbations/       # Drexpa-generated perturbation profiles
├── drugpanel/           # Drexpa-generated drug panel
└── modeloutputs/        # Model output nodes used as viability proxies
```

If sampling is used, Oris may also use or generate:

```text
src/SampledModels/
```

**Config file:** `config/oris.toml`

The Oris configuration file controls SLURM settings, environment setup, media constraints, and simulation timeouts. The most important fields to check before running are:

* SLURM partition/account
* module load or conda activation commands
* `media_targets`
* `timeout_sampling`
* `timeout_paths`

**Run:**

Before running Oris, install it on the HPC system or in the same Python environment used by the SLURM job.

Installation instructions are available in the Oris documentation:  
https://druglogics.github.io/trafikk/oris/installation.html

Quick install:

```bash
pip install git+https://github.com/druglogics/oris.git
oris --help
```

To run Oris in synergy mode:

```bash
oris --zips runs/04_oris/zips --mode synergies --sampling 10 --config config/oris.toml
```

To compute path counts for all Boolean model nodes:

```bash
oris --zips runs/04_oris/zips --mode countpaths --sampling 10 --config config/oris.toml
```

To compute both synergy scores and full path counts:

```bash
oris --zips runs/04_oris/zips --mode full --sampling 10 --config config/oris.toml
```

**Modes:**

| Mode         | Description                                                                               | Main outputs                          |
| ------------ | ----------------------------------------------------------------------------------------- | ------------------------------------- |
| `synergies`  | Computes path counts toward model output nodes and calculates Bliss synergy excess scores | `PathCounts.txt`, `SynergyExcess.txt` |
| `countpaths` | Computes path counts toward all Boolean model nodes                                       | `PathCountsFull.txt`                  |
| `full`       | Runs both synergy scoring and full path counting                                          | all three output files                |

**Expected outputs:**

Oris augments each input ZIP file with a new `Results/` directory.

Depending on the selected mode, the ZIP file may contain:

```text
Results/
├── PathCounts.txt        # Path counts toward model output nodes
├── SynergyExcess.txt     # Bliss synergy excess scores
└── PathCountsFull.txt    # Path counts toward all Boolean model nodes
```

**Logs:**

If running through SLURM, check the generated log files:

```text
oris_*.out
oris_*.err
```

**What's next:** Oris outputs are benchmarked by Synco and analyzed by Siflex.

---
WORK-IN-PROGRESS (from here down)
---

### Step 5: Synco — Benchmarking

**Purpose:** Compare *in silico* predictions against experimental synergy data.

**Inputs:**
- Oris output: `runs/04_oris/` (ZIPs with Results/)
- Experimental synergy data: `data/raw/drugs/synergy_data.csv`

**Config file:** `config/synco.json`

**Run:**
```bash
synco --config config/synco.json
```

**Alternative (Jupyter notebook mode):**
```bash
jupyter notebook notebooks/synco_analysis.ipynb
```

**Expected outputs** in `runs/05_synco/`:
- `metrics.csv` — AUC-ROC, AUC-PR, F1, accuracy, recall, precision
- `roc_curve.csv` — ROC curve coordinates
- `pr_curve.csv` — Precision-Recall curve coordinates
- `confusion_matrix.csv` — TP, FP, TN, FN
- `results_summary.html` — Interactive report
- Logs: `synco.log`

**What's next:** Siflex uses the benchmarked results for pathway analysis.

---

### Step 6: Siflex — Pathway Analysis & Interactive Visualization

**Purpose:** Identify pathway-level mechanisms of drug synergy and generate interactive dashboards.

**Inputs:**
- Oris output with synergy scores: `runs/04_oris/`
- KEGG pathway data (downloaded automatically or provide mappings)
- Tissue context (from Drexpa metadata)

**Config file:** `config/siflex.json`

**Run:**
```bash
siflex --config config/siflex.json
```

**Expected outputs** in `runs/06_siflex/`:
- `networks/{CellLine}_network.html` — Interactive network explorer (open in browser)
- `pathways/{CellLine}_pathways.html` — Pathway impact analysis
- `results.json` — Raw analysis data
- Logs: `siflex.log`

**View results:**
```bash
# Open in browser
open runs/06_siflex/networks/*.html
# Or with Python's built-in server
python -m http.server --directory runs/06_siflex 8000
# Then visit http://localhost:8000
```

---

## Advanced Usage

### Skip Steps & Jump to a Specific Stage

You don't need to run all steps. If you already have outputs from an earlier step, you can start later:

**Example: Start at Drexpa (skip Celios & Gitsbe)**

1. Copy pre-existing Gitsbe ZIPs to `runs/02_gitsbe/`
2. Copy pre-existing Celios outputs to `runs/01_celios/`
3. Edit `config/drexpa.json` with correct input paths
4. Run: `drexpa --config config/drexpa.json`

**Example: Run only Oris (already have Drexpa outputs)**

1. Copy Gitsbe ZIPs to `runs/02_gitsbe/`
2. Copy Drexpa outputs to `runs/03_drexpa/`
3. Edit `config/oris.toml` with correct paths
4. Run: `oris --zips ...` (see Step 4)

### Reuse Outputs Across Projects

Outputs are self-contained, so you can link them:

```bash
# Link another project's Celios output
ln -s /path/to/other_project/runs/01_celios runs/01_celios

# Run Gitsbe with linked input
gitsbe --config config/gitsbe.yaml
```

### Run on HPC with SLURM

Edit `config/oris.toml`:
- Change `partition` to your queue name
- Change `account` to your project account
- Update `module load` lines for your environment
- Set `auto_submit = true` (Oris will submit the job automatically)

Then run:
```bash
oris --config config/oris.toml --zips runs/02_gitsbe/*.zip --mode full
```

Or submit manually:
```bash
sbatch slurm/oris_jobs/run_oris.sh
```

---

## Checking Project Status

Run the status checker at any time to see which steps are complete:

```bash
python scripts/trafikk_status.py
```

**Output:**
```
TRAFIKK Project Status
======================

[✓] Raw data found (42 files)
[✓] Celios: Complete
[✓] Gitsbe: Complete
[✓] Drexpa: Complete
[ ] Oris: Pending
[ ] Synco: Pending
[ ] Siflex: Pending

Next step: Run Oris
  Command: oris --config config/oris.toml --mode synergies
```

---

## Troubleshooting

### Celios: "Node dictionary not found"

**Fix:** Make sure `data/raw/networks/your_network.sif` and `data/raw/hgnc/hgnc_complete_set.txt` exist.

### Gitsbe: "Input activity matrix not found"

**Fix:** Check that Celios finished successfully and outputs exist in `runs/01_celios/`.

### Drexpa: "ChEMBL resolution failed"

**Cause:** Network timeout or unknown drug name.

**Fix:**
- Check drug names in `data/raw/drugs/drug_names.txt` (must match ChEMBL exactly)
- Provide manual mappings in `data/raw/drugs/manual_chembl.csv` to skip network queries
- Run with `--verbose` to see which drugs failed

### Oris: SLURM job fails with module error

**Cause:** Module names don't match your HPC system.

**Fix:**
1. Check available modules: `module avail`
2. Edit `config/oris.toml` `[env].preamble` section
3. Replace module names with correct versions for your system

### "Permission denied" on SLURM scripts

**Fix:**
```bash
chmod +x slurm/gitsbe_jobs/run_gitsbe_array.sh
chmod +x slurm/oris_jobs/run_oris.sh
```

### Output files are empty or missing

**Fix:** Check logs for errors:
```bash
cat runs/01_celios/celios.log
cat logs/slurm_*.err
```

---

## Configuration Reference

### project.yaml

Project-level metadata (for reference only, not used by TRAFIKK tools).

```yaml
project_name: "MyProject"
description: "Study of drug synergy in breast cancer"
tissue: "Breast"
cell_lines: ["MCF7", "T47D"]
date_created: "2025-01-15"
```

### celios.yaml

See `config/celios.yaml` — paths to network, omics data, HGNC symbols.

### drexpa.json

See `config/drexpa.json` — drug file paths, column names, synergy threshold.

### oris.toml

See `config/oris.toml` — SLURM directives, HPC environment, sampling parameters.

### synco.json

See `config/synco.json` — metrics to calculate, thresholds.

### siflex.json

See `config/siflex.json` — pathway databases, dashboard ports, tissue context.

---

## Tips for Best Results

1. **Validate inputs early:** Run Celios first to catch data issues before long Gitsbe/Oris runs.

2. **Use SLURM for Oris:** Oris is HPC-optimized. Even 50-100 models benefit from parallel computation.

3. **Save intermediate outputs:** Don't delete `runs/XX_*/` folders. They're needed by later steps.

4. **Organize by tissue:** If running multiple tissues, copy the template:
   ```bash
   cp -r my_trafikk_project my_trafikk_project_tissue2
   ```

5. **Check Synco early:** Benchmarking reveals prediction quality before investing in Siflex analysis.

---

## Output Summary

| Step | Output Type | Where | Used By |
|------|---|---|---|
| Celios | Activity matrices (CSV) | `runs/01_celios/` | Gitsbe |
| Drexpa | Perturbation profiles (TXT) | `runs/02_drexpa/` | Oris |
| Gitsbe | Model ensembles (ZIP) | `runs/03_gitsbe/` | Drexpa, Oris |
| Oris | Synergy scores (ZIP → Results/) | `runs/04_oris/` | Synco, Siflex |
| Synco | Metrics & curves (CSV, HTML) | `runs/05_synco/` | Reporting |
| Siflex | Interactive dashboards (HTML) | `runs/06_siflex/` | Visualization |

---

## Getting Help

- **TRAFIKK Documentation:** https://druglogics.github.io/trafikk/
- **Module Repos:**
  - Celios: https://github.com/druglogics/celios
  - Gitsbe: https://github.com/druglogics/gitsbe
  - Drexpa: https://github.com/druglogics/drexpa
  - Oris: https://github.com/druglogics/oris
  - Synco: https://github.com/ViviamSB/SYNCO
  - Siflex: https://github.com/druglogics/siflex

---

## Citation

If you use this pipeline, please cite:

> Fariñas M., Bermúdez V., Tsirvouli E., Lippestad K., Zobolas J., Aittokallio T., Lehti K., Flobak Å.
> **TRAFIKK: systematic prediction and mechanistic interpretation of anticancer drug synergies.**
> *Submitted.*

---

**Last updated:** 2026-06-19
