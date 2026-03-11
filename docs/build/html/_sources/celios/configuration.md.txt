# Configuration

Celios is entirely controlled via JSON or YAML configuration files, making it easy to reproduce analyses and scale to multiple datasets.

## 🔀 Pipeline behaviour

**Scenario 1: `"Node"` step is defined in config**
- STEP 1 will run (Node dictionary generation), even if `node_dic` is also in Activity
- The generated node dictionary will be used for Activity extraction

**Scenario 2: `"Node"` step is NOT defined, but `node_dic` is in Activity config**
- STEP 1 is skipped
- The provided CSV file is loaded and used directly

**Scenario 3: Neither `"Node"` step nor `node_dic` is provided**
- The pipeline will raise an error (no node dictionary source available)

## 📄 Configuration example

```json
{
    "paths": {
        "base": ".",
        "input": "data",
        "output": "results",
        "cellfiles_dir": "results/cell_lines",
        "tissue_dir": "results/tissue_folders"
    },
    "steps": {
        "Node": {
            "node_input": "node_dic_input/DNAdamage.sif",
            "hgnc_symbols_file": "node_dic_input/hgnc_complete_set.txt",
            "manual_symbols_file": "node_dic_input/manual_symbols.csv",
            "include_alias_previous_symbols": false,
            "directory_output": "results"
        },
        "Activity": {
            "activity_file": "activity_input/rnaseq_tpm_20220624.csv",
            "cell_line_file": "activity_input/cell_line_list.csv",
            "tf_activity_file": "activity_input/ccle_tf_activities.csv",
            "mutations_file": "activity_input/CCLE_muts_binary.csv",
            "cnv_file": "activity_input/CCLE_CNV_binary.csv",
            "directory_output": "results",
            "data_sources": ["mutations", "cnv", "TF"]
        }
    }
}
```

## 💡 Notes

- **YAML support** — YAML config files require `pyyaml` in your environment (optional). JSON configs work without extra packages.
- **Example configurations** — See `tests/test_run_celios.py`, `tests/celios_consensus.py`, and `tests/celios_hgsoc.py` for real-world examples.
- **Interactive tutorials** — See `notebooks/1_select_visualize.ipynb` for a step-by-step walkthrough.
