# TRAFIKK Project Template

A structured, step-by-step guide for running the complete TRAFIKK pipeline on your data.

## Overview

This project template guides you through all 6 stages of the TRAFIKK pipeline:

```
Celios ➜ Gitsbe ➜ Drexpa ➜ Oris ➜ Synco ➜ Siflex
 Omics    Models   Drugs   Synergy  Bench  Analysis
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
│   ├── 02_gitsbe/       # Boolean model ensembles
│   ├── 03_drexpa/       # Drug panels & perturbation profiles
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

### 1. Prepare Your Raw Data

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

### 2. Edit Configuration Files

Each step has a configuration file in `config/`:

- `project.yaml` — Project metadata
- `celios.yaml` — Step 1: Network calibration
- `gitsbe.yaml` — Step 2: Model generation
- `drexpa.json` — Step 3: Drug mapping
- `oris.toml` — Step 4: Synergy scoring (with SLURM settings)
- `synco.json` — Step 5: Benchmarking
- `siflex.json` — Step 6: Visualization

Edit each config with your file paths and parameters. **Templates are provided with placeholders.**

### 3. Run Each Step

See sections below for each step.

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
- `cell_lines/` — Activity matrices per cell line (CSV files)
- `tissue_folders/` — Tissue-organized output (if configured)
- `node_dictionary.csv` — Gene → node mappings
- Logs: `celios.log`

**What's next:** Outputs feed into Gitsbe as calibrated activity profiles.

---

### Step 2: Gitsbe — Boolean Model Ensemble Generation

**Purpose:** Generate a diverse ensemble of Boolean models for each cell line using genetic algorithm optimization.

**Inputs:**
- Celios output: cell-line-specific activity matrices from `runs/01_celios/cell_lines/`

**Config file:** `config/gitsbe.yaml`

**Run (local):**
```bash
gitsbe --config config/gitsbe.yaml
```

**Run (HPC with SLURM):**
```bash
sbatch slurm/gitsbe_jobs/run_gitsbe_array.sh
```

**Expected outputs** in `runs/02_gitsbe/`:
- One ZIP file per cell line: `{CellLine}_models.zip`
- Each ZIP contains: models.txt, attractors.txt, etc.
- Logs: `gitsbe_*.out`, `gitsbe_*.err` (if SLURM)

**What's next:** Model ensembles (ZIPs) are used by Drexpa and Oris.

---

### Step 3: Drexpa — Drug Panel & Perturbation Mapping

**Purpose:** Map drugs to network nodes and generate perturbation profiles.

**Inputs:**
- Gitsbe output: ZIPs from `runs/02_gitsbe/`
- Drug names file: `data/raw/drugs/drug_names.txt`
- (Optional) Experimental synergy data: `data/raw/drugs/synergy_data.csv`
- Node dictionary: from Celios (`runs/01_celios/node_dictionary.csv`)
- Tissue-cellline mapping: `data/raw/metadata/tissue_cellline_map.csv`

**Config file:** `config/drexpa.json`

**Run:**
```bash
drexpa --config config/drexpa.json
```

**Expected outputs** in `runs/03_drexpa/`:
- `drug_ChEMBL_IDs.csv` — Drug → ChEMBL ID mapping
- `drug_node_targets.csv` — Drug → node targets
- `drug_panel_df.csv` — Summary of all drugs
- `{TISSUE}/perturbations.txt` — Per-tissue perturbation profiles
- `{TISSUE}/synergies.csv` — Per-tissue synergy data (if provided)
- Logs: `drexpa.log`

**What's next:** Perturbation files are inputs to Oris.

---

### Step 4: Oris — Synergy Scoring via Signal Propagation

**Purpose:** Compute *in silico* viability and synergy scores for all drug combinations.

**Inputs:**
- Gitsbe ZIPs: `runs/02_gitsbe/{CellLine}_models.zip`
- Drexpa perturbation files: `runs/03_drexpa/{TISSUE}/perturbations.txt`

**Config file:** `config/oris.toml` (includes SLURM settings)

**Run (local, single cell line):**
```bash
oris --zips runs/02_gitsbe/MyCell_models.zip --mode synergies --sampling 50
```

**Run (HPC with SLURM, multiple cell lines):**
```bash
sbatch slurm/oris_jobs/run_oris.sh
```

**Expected outputs** in `runs/04_oris/`:
- Input ZIPs augmented with `Results/` directory:
  - `Results/SynergyExcess.txt` — Bliss synergy scores per drug pair
  - `Results/PathCounts.txt` — Signal path statistics
- Logs: `oris_*.out`, `oris_*.err` (if SLURM)

**What's next:** Oris outputs are benchmarked by Synco and analyzed by Siflex.

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
| Gitsbe | Model ensembles (ZIP) | `runs/02_gitsbe/` | Drexpa, Oris |
| Drexpa | Perturbation profiles (TXT) | `runs/03_drexpa/` | Oris |
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

**Last updated:** 2025-05-05
