# Configuration

## 📜 Default config structure

```json
{
  "global": {
    "output_dir": "output",
    "verbose": false,
    "save": true,
    "base_data_dir": "data"
  },
  "paths": {
    "drug_names_file": "drug_names.txt",
    "synergy_data_file": "synergy_data.csv",
    "node_dict_file": "node_dict.csv",
    "tissue_cline_file": "tissue_cline.csv",
    "db_file": null,
    "manual_chembl_csv": "manual_chembl.csv"
  },
  "columns": {
    "drug_name": "drug_name",
    "drug_name_A": "drug_name_A",
    "drug_name_B": "drug_name_B",
    "conc_A": "conc_A",
    "conc_B": "conc_B",
    "cell_line": "cell_line",
    "synergy": "synergy"
  },
  "options": {
    "synergy_threshold": 0.0,
    "double_drug_screen": true,
    "original_target_merge": "fill_missing"
  }
}
```

## 💡 Key points

- `db_file: null` → Uses internal package database (managed by project, not user).
- `base_data_dir` — Base path; all relative paths are resolved against it.
- `columns` — Customise column names if your data uses different headers.
- Deep-merge override: Custom config merges recursively with defaults; only specified sections override.

## 📐 Data format specifications

### Drug names file

Plain text, one drug per line:

```
Aspirin
Ibuprofen
Paracetamol
```

### Node dictionary (CSV)

Gene/protein symbols mapped to logical model node names:

```text
gene,node
EGFR,EGFR_node
TP53,p53
BRAF,BRAF_node
```

### Synergy data (CSV)

**With concentration data** (dual-drug screening):

```text
drug_name_A,drug_name_B,conc_A,conc_B,tissue,cell_line,synergy
Aspirin,Ibuprofen,1.0,2.0,Breast,MCF7,0.15
```

**Without concentration data** (single-dose combinations):

```text
drug_name_A,drug_name_B,tissue,cell_line,synergy
Aspirin,Ibuprofen,Breast,MCF7,0.15
```

### Tissue-cell line mapping (CSV)

```text
tissue,cell_line
Breast,MCF7
Breast,T47D
Colorectal,HCT116
```

## 🔧 Advanced features

### Manual ChEMBL mapping

Provide a CSV to override ChEMBL resolution (skip network queries):

```text
drug_name,ChEMBL_ID
Aspirin,CHEMBL25
Ibuprofen,CHEMBL521
```

Configure in `paths.manual_chembl_csv`.

### Verbose logging & timing

```bash
drexpa --config my_config.json --verbose
```

Output includes:
- Step start/end timestamps
- Per-step duration (seconds)
- Preflight warnings & validation details
- Pipeline summary

## ❓ Troubleshooting

### Missing required files

**Error:** `FileNotFoundError: Preflight validation failed. Missing required files`
**Fix:** Check file paths in config. Ensure `base_data_dir` is correct.

### Missing required columns

**Error:** `ValueError: Missing required columns in synergy data`
**Fix:** Verify `columns` section in config matches your data headers. Use `--verbose` to see exact missing columns.

### ChEMBL resolution fails

**Error:** Network timeout or no results for drug name
**Fix:**
- Check drug name spelling (must match ChEMBL exactly or be unambiguous).
- Provide manual ChEMBL mapping in `manual_chembl.csv` to skip network queries.
- Run with `--verbose` to see which drugs failed.
