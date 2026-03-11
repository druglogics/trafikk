<div align="center">

# 🧬 TRAFIKK

**Systematic prediction and mechanistic interpretation of anticancer drug synergies**

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-6c3ec1.svg)](LICENSE)
[![Docs](https://img.shields.io/badge/docs-GitHub%20Pages-4a1d96.svg)](https://druglogics.github.io/trafikk/)
[![Built with](https://img.shields.io/badge/built%20with-DrugLogics-e84393.svg)](https://github.com/druglogics)

</div>

---

Trafikk is a computational pipeline for *in silico* prediction and mechanistic interpretation of drug combination responses in cancer. It integrates cell-line-specific molecular contexts with Boolean network modelling and signal-propagation analysis to identify synergistic drug pairs and explain how synergy emerges at the pathway level.

<p align="center">
  <img src="src/overview.svg" alt="Pipeline overview" width="720" />
</p>

## ⚙️ Pipeline

Trafikk simulates drug perturbations on cell-line-calibrated Boolean models of cancer signalling networks, generating functional response profiles for single drugs and combinations. These profiles enable both synergy classification and mechanistic interpretation of the underlying signalling dynamics.

```text
 Celios ➜ Gitsbe ➜ Drexpa ➜ Oris ➜ Synco ➜ Siflex
   │         │         │        │       │        │
 Omics    Models    Drugs    Synergy  Bench   Analysis
```

### Modules

| | Module | What it does | Language |
|---|---|---|---|
| 🧬 | [**Celios**](https://github.com/druglogics/celios) | Integrates cell-line omics data (mutations, CNV, TF activity) to calibrate the base network to specific biological contexts | Python |
| 🔧 | [**Gitsbe**](https://github.com/druglogics/gitsbe) | Generates ensembles of logic-based models for each calibrated cell-line network | Java |
| 💊 | [**Drexpa**](https://github.com/druglogics/drexpa) | Maps experimental drug panels to *in silico* perturbation profiles using public target databases (GDSC, OpenTargets, ChEMBL, UniProt, BindingDB) | Python |
| ⚡ | [**Oris**](https://github.com/druglogics/oris) | Computes *in silico* viability and synergy scores via signal-propagation analysis (built on [BooLEVARD](https://github.com/farinasm/boolevard)) | Python · HPC |
| 📊 | [**Synco**](https://github.com/ViviamSB/SYNCO) | Benchmarks predictions against experimental synergy data using standard classification metrics (AUC-ROC, AUC-PR, F1, accuracy, recall, precision) | Python |
| 🔬 | [**Siflex**](https://github.com/druglogics/siflex) | Performs pathway-level functional analysis of drug effects and generates mechanistic hypotheses for synergistic responses | Python |

## 🚀 Installation

Each module is installed independently from its own repository:

```bash
# Python modules
pip install git+https://github.com/druglogics/celios.git
pip install git+https://github.com/druglogics/drexpa.git
pip install git+https://github.com/druglogics/oris.git
pip install git+https://github.com/druglogics/siflex.git

# Synco (notebook-based)
pip install git+https://github.com/ViviamSB/SYNCO.git

# Gitsbe — see its repo for Java build instructions
# https://github.com/druglogics/gitsbe
```

> Refer to each module's repository for detailed dependency and environment requirements.

## 📖 Documentation

Full unified documentation is available at **[druglogics.github.io/trafikk](https://druglogics.github.io/trafikk/)**.

## 🧪 Synergy quantification

Drug synergy is assessed using **Bliss independence**:

$$\Delta_{\text{Bliss}} = V_{AB} - V_A \cdot V_B$$

where $V_{AB}$ is the viability under combined perturbation and $V_A$, $V_B$ are the single-drug viabilities. Negative values indicate synergy.

## 🏗️ Built upon

| Project | Role |
|---|---|
| [DrugLogics](https://github.com/druglogics) | Model generation and calibration |
| [BooLEVARD](https://github.com/farinasm/boolevard) | Signal-propagation analysis in Boolean models |

## 📝 Citation

> Fariñas M.\*, Bermúdez V.\*, Tsirvouli E., Lippestad K., Zobolas J., Aittokallio T., Lehti K.†, Flobak Å.†
> **TRAFIKK: systematic prediction and mechanistic interpretation of anticancer drug synergies.**
> *Submitted.*

## 📄 License

This project is licensed under the [GNU General Public License v3.0](LICENSE).
