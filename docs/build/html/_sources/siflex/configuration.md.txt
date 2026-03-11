# Configuration

Siflex is configured via a JSON file specifying input/output paths and pipeline steps.

## 📜 Configuration file

```json
{
  "input_files": {
    "sif_network": "data/cell_fate_plus.sif",
    "node_hgnc_file": "data/NodeHGNC.csv",
    "kegg_pathway": "data/kegg_pathway.csv",
    "kegg_categories": "data/kegg_categories.json",
    "bless_out": "data/tissue_folders",
    "inhibitor_profiles": "data/inhibitor_profiles.csv"
  },
  "output_files": {
    "node_scores": "output/node_scores.csv",
    "node_scores_agg": "output/node_scores_agg.csv",
    "pathway_scores": "output/pathway_scores.csv",
    "synergy_scores": "output/synergy_scores.csv",
    "node_pathway_index": "output/node_pathway_index.json",
    "pathway_catalog": "output/pathway_catalog.json"
  },
  "steps": {
    "calculate_scores": true,
    "prepare_scores": true
  }
}
```

## 📐 Input data formats

### SIF network file

Tab-separated file with three columns:

```
source_node    interaction_type    target_node
EGFR           activate            MAPK1
PI3K           inhibit             PTEN
```

### ORIS output

Directory structure with tissue folders containing cell line subdirectories:

```
tissue_folders/
├── lung/
│   ├── A549/
│   │   └── Pairwise_comparison.tsv
│   └── H1299/
│       └── Pairwise_comparison.tsv
└── breast/
    └── MCF7/
        └── Pairwise_comparison.tsv
```

### Node-HGNC mapping (NodeHGNC.csv)

```
Node,HGNC
EGFR,EGFR
MAPK,MAPK1
```

### KEGG pathway file (kegg_pathway.csv)

```
pathway_id,pathway_name,gene_symbols
hsa04010,MAPK signaling pathway,"EGFR,MAPK1,RAF1"
```

## 🏗️ Architecture

Siflex follows a modular architecture with clean separation of concerns:

- **Data Layer** (`features/`): Data loading, transformation, and score calculation
- **Application Layer** (`apps/`): Data preparation functions for each explorer
- **Presentation Layer** (`apps/*_dash.py`): Dash-based interactive visualisations
- **Orchestration Layer** (`main.py`): Pipeline coordination and CLI interface

```
SIFLEX/
├── siflex/
│   ├── cli.py                  # Command-line interface
│   ├── config.py               # Configuration management
│   ├── main.py                 # Pipeline orchestration
│   ├── apps/
│   │   ├── network_explorer.py # Network data preparation
│   │   ├── network_dash.py     # Network visualisation
│   │   ├── pathway_explorer.py # Pathway data preparation
│   │   ├── pathway_dash.py     # Pathway visualisation
│   │   └── app_style.py        # Shared styling
│   └── features/
│       ├── calculate_scores.py # Score calculation logic
│       ├── prepare_scores.py   # Data preparation
│       └── data_utils.py       # Data loading utilities
├── tests/
├── data/
├── output/
└── pyproject.toml
```
