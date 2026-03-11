# Usage

## 🚀 Running the full pipeline

### Via CLI (recommended)

Run the pipeline from the repository root with a configuration file (JSON or YAML):

```bash
python -m celios.cli run --config path/to/config.yaml --verbose
```

Options:

- `--config` (required): Path to pipeline config (JSON or YAML)
- `--verbose`: Print detailed output
- `--plan`: Only print execution plan without running
- `--stop-after`: Stop execution after a specific step

### Via Python script 🐍

```python
from celios.core import run_celios

config = {
    "paths": {
        "base": ".",
        "input": "data",
        "output": "results",
        "cellfiles_dir": "results/cell_lines",
    },
    "steps": {
        "Node": {
            "node_input": "node_dic_input/DNAdamage.sif",
            "hgnc_symbols_file": "node_dic_input/hgnc_complete_set.txt",
            "manual_symbols_file": "node_dic_input/manual_symbols.csv",
            "include_alias_previous_symbols": False,
            "directory_output": "results",
        },
        "Activity": {
            "activity_file": "activity_input/rnaseq_tpm_20220624.csv",
            "cell_line_file": "activity_input/cell_line_list.csv",
            "tf_activity_file": "activity_input/ccle_tf_activities.csv",
            "mutations_file": "activity_input/CCLE_muts_binary.csv",
            "cnv_file": "activity_input/CCLE_CNV_binary.csv",
            "directory_output": "results",
            "data_sources": ["mutations", "cnv", "TF"],
        },
    },
}

artifacts = run_celios(config=config, plan=False, verbose=True)
```

## 🗂️ Tissue-organised output

Celios supports organising DrugLogics training files by tissue type. When `paths.tissue_dir` is specified, training files are written to `tissue_dir/<Tissue>/<cell_line_name>/` based on the tissue information in `cell_line_file`.

```yaml
paths:
  tissue_dir: "results/tissue_folders"
steps:
  Activity:
    cell_line_file: "data/cell_line_list.csv"
```

The CSV file must include columns for tissue, SIDM (unique identifier), and cell_line_name when using tissue-organised output.

## ⏭️ Skipping the Node step

If you already have a pre-built node dictionary file, you can skip the Node step by:

1. **Omitting** the `"Node"` section from `steps` in your config
2. **Adding** `"node_dic"` to the `Activity` section pointing to your CSV file

```python
config = {
    "paths": {
        "base": ".",
        "input": "data",
        "output": "results",
    },
    "steps": {
        "Activity": {
            "node_dic": "path/to/NODE_HGNC_equivalences.csv",
            "activity_file": "activity_input/rnaseq_tpm_20220624.csv",
            # ... other activity config ...
        },
    },
}

artifacts = run_celios(config=config, verbose=True)
```

## 🔧 Feature helpers

Call Node helpers directly with CLI subcommands:

```bash
python -m celios.cli node-from-sif --sif examples/DNAdamage.sif \
    --hgnc examples/hgnc_complete_set.txt --out results/node_dict.csv

python -m celios.cli node-from-object --input "TP53,BRCA1,EGFR" \
    --hgnc examples/hgnc_complete_set.txt --out results/node_dict.csv \
    --include_alias_prev
```
