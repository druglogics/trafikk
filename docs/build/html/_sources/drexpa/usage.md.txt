# Usage

## 🚀 Quick start (CLI)

### 📁 Prepare input files

```
data/
├── drug_names.txt           # One drug per line
├── node_dict.csv            # Gene → Node mapping
└── synergy_data.csv         # Optional: drug combinations + effects
```

### 📝 Create config file

`my_config.json`:

```json
{
  "global": {"output_dir": "results", "base_data_dir": "data"},
  "paths": {
    "drug_names_file": "drug_names.txt",
    "node_dict_file": "node_dict.csv",
    "synergy_data_file": "synergy_data.csv"
  },
  "options": {"double_drug_screen": true}
}
```

### ▶️ Run pipeline

```bash
# Full pipeline
drexpa --config my_config.json

# Generate profiles only
drexpa --config my_config.json --until profiles

# Specific steps
drexpa --config my_config.json --steps profiles,panel

# Verbose mode (structured logging + timing)
drexpa --config my_config.json --verbose
```

## ⌨️ CLI options

| Option | Description | Example |
|--------|-------------|---------|
| `--config PATH` | Custom config JSON file | `--config my_config.json` |
| `--synergy-data PATH` | Override synergy data file | `--synergy-data screen.csv` |
| `--output-dir DIR` | Override output directory | `--output-dir ./results` |
| `--until STEP` | Run until step (inclusive) | `--until panel` |
| `--steps STEPS` | Specific steps (comma-separated) | `--steps profiles,panel` |
| `--verbose` | Enable structured logging + timing | `--verbose` |

## 🔄 Pipeline steps

1. `load_data` — Load synergy data
2. `chembl_ids` — Resolve ChEMBL IDs (requires ChEMBL network access)
3. `doses` — Extract & process drug doses (requires concentration columns)
4. `targets` — Query internal drug-target database
5. `node_targets` — Map targets to logical model nodes
6. `profiles` — Generate unique drug profiles with Pipeline IDs
7. `combinations` — Prepare drug combinations (requires synergy data)
8. `panel` — Create drug panel (DrugLogics format)
9. `perturbations` — Generate perturbation files per condition
10. `synergies` — Process observed synergies

Dependencies are resolved automatically: `--until panel` runs steps 1–8 with all prerequisites.

## 🐍 Python API

```python
from drexpa import run_pipeline

config = {
    "global": {"output_dir": "results"},
    "paths": {
        "drug_names_file": "data/drugs.txt",
        "node_dict_file": "data/nodes.csv",
    }
}

# Full pipeline
run_pipeline(config_dict=config)

# Specific steps
run_pipeline(
    config_dict=config,
    synergy_data_file="data/synergy.csv",
    steps_to_run=["profiles", "panel"],
)
```

## 📦 Output files

| File | Step | Content |
|------|------|---------|
| `drug_ChEMBL_IDs.csv` | `chembl_ids` | Drug name → ChEMBL ID mapping |
| `drug_ChEMBL_doses.csv` | `doses` | Drugs with IC50 concentrations |
| `drug_ChEMBL_targets.csv` | `targets` | Drug → Targets from database |
| `drug_node_targets.csv` | `node_targets` | Drug → Logical model nodes |
| `drug_profiles.csv` | `profiles` | Drug profiles with Pipeline IDs |
| `drug_panel_df.csv` | `panel` | Drug panel (DrugLogics format) |
| `drugpanel` | `panel` | Formatted drug panel file |
| `<TISSUE>/` | `perturbations` | Per-tissue perturbation files |
