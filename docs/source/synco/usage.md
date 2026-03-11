# Usage

## 📓 Notebook workflow (exploratory)

1. Create and activate the environment (see [Installation](installation.md)).
2. Open the notebook `synco_plots.ipynb`.
3. Prepare the `CONFIG` to read your data and options:
   - `paths`: base, pipeline_runs, input, output
   - `general`: cell_lines, run_date, verbose
   - `compare`: prediction_method (DrugLogics or BooLEVARD), threshold, synergy_column, analysis_mode (inhibitor_combination or cell_line)
4. Run cells to build and extract results, make ring plots and ROC or PR curves.

## 🖥️ CLI — run from terminal

You can run Synco either with a configuration file (JSON or YAML) or using a lightweight direct-arguments mode.

### 📄 Config-file mode (recommended for reproducibility)

```bash
# Preview execution plan
python -m synco -c examples/synco_example_config.json --plan

# Run analysis
python -m synco -c examples/synco_example_config.json
```

### ⚡ Direct-arguments mode (no config file)

```bash
python -m synco --base data/DrugLogics \
    --pipeline-runs data/sample_raw/20250804/drabme_out \
    --input data/synco_input \
    --output results \
    --cell-lines C2BBE1,CAR1,T84 \
    --prediction-method DrugLogics \
    --plan
```

### 🔀 Override synergies file

Specify the exact experimental synergies file to use with `--synergies_filename` (accepts a filename relative to the `--input` folder or an absolute path):

```bash
python -m synco -c examples/synco_example_config.json \
    --synergies_filename data/synco_input/labdata_nochemo_hsa.csv --plan
```

## ⚙️ Configuration options

| Section | Key | Description |
|---------|-----|-------------|
| `paths` | `base` | Base directory for pipeline data |
| `paths` | `pipeline_runs` | Path to pipeline prediction outputs |
| `paths` | `input` | Path to experimental synergy data |
| `paths` | `output` | Output directory for results |
| `general` | `cell_lines` | List of cell lines to analyse |
| `general` | `run_date` | Date identifier for the run |
| `general` | `verbose` | Print detailed output |
| `compare` | `prediction_method` | DrugLogics or BooLEVARD |
| `compare` | `threshold` | Synergy classification threshold |
| `compare` | `synergy_column` | Column name for synergy scores |
| `compare` | `analysis_mode` | `inhibitor_combination` or `cell_line` |
