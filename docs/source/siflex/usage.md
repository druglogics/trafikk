# Usage

## 🚀 Quick start

### ▶️ Full pipeline (calculate scores + explore)

```bash
python -m siflex.main config.json
```

### 📊 Calculate scores only

```bash
python -m siflex.main config.json --explore=none
```

### 🌐 Explore network only (skip calculation)

```bash
python -m siflex.main config.json --no-calculate --explore=network
```

### 🧬 Explore pathways only

```bash
python -m siflex.main config.json --no-calculate --explore=pathways
```

### 🔄 Run both explorers simultaneously

```bash
python -m siflex.main config.json --no-calculate --explore=all
```

- Network explorer: `http://localhost:8050`
- Pathway explorer: `http://localhost:8051`

## ⌨️ CLI options

```
python -m siflex.main <config_path> [OPTIONS]

Required:
  config_path              Path to configuration JSON file

Options:
  --no-calculate          Skip score calculation (use existing results)
  --explore=<mode>        Exploration mode: network, pathways, all, or none
                          (default: all)
```

## 🖱️ Network explorer

The network explorer provides three independent visualisation panels for comparing signalling networks across different conditions:

- **Tissue Selection**: Choose from 26+ cancer tissue types
- **Cell Line Filtering**: Filter by specific cell lines within tissues
- **Condition Comparison**: Compare drug responses across experimental conditions
- **Pathway Highlighting**: Overlay KEGG pathway membership with pie chart visualisations
- **Interactive Network**: Pan, zoom, and hover over nodes to see synergy scores

## 🧬 Pathway explorer

The pathway explorer offers two side-by-side panels for comparing pathway impacts:

- **Drug Combination Selection**: Choose two drugs to analyse
- **Aggregation Methods**: mean, median for node score aggregation
- **Pathway Ranking**: Automatically sort by impact score
- **Flip Analysis**: Identify pathways with opposite responses (synergistic effects)
- **Interactive Plots**: Hover to see detailed pathway information

## 🐍 Python API

```python
from siflex.main import run_siflex, build_config

# Load configuration
config = build_config("config.json")

# Run with custom options
run_siflex(
    config,
    config_path="config.json",
    calculate=True,
    explore="all",
    run_server=True,
)
```

### 🧩 Using individual components

```python
from siflex.apps import prepare_network_data, run_network_dash

# Prepare network data
nodes, edges, node_pathway_index, PATHWAY_CATALOG, NODE_TO_PATHS, \
    TISSUE_OPTIONS, CELL_LINES_BY_TISSUE, conditions, COND_LABELS, \
    node_scores_agg = prepare_network_data(config_path="config.json")

# Run dashboard on custom port
run_network_dash(
    nodes, edges, node_pathway_index, PATHWAY_CATALOG, NODE_TO_PATHS,
    TISSUE_OPTIONS, CELL_LINES_BY_TISSUE, conditions, COND_LABELS,
    node_scores_agg,
    run_server=True,
    port=8080,
)
```
