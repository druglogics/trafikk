# Initial Conditions

Bless reduces the state space prior to simulation by applying:

1. **Media constraints**
2. **Calibration-based initial conditions**

---

### 1. Media constraints

Media constraints depend on the experimental culture medium and are explicitly defined by the user in the configuration file (see [*Configuration*](configuration.md)). If the medium contains a **ligand**, **activator**, or **repressor** for a model node:

- a dedicated **input node** is created,
- a Boolean equation describing its effect is assempled,
- and stable states in which that node is **active** are retained when required for downstream analyses.

---

### 2. Calibration-Based Initial Conditions

{ref}`Gitsbe <gitsbe-home>` generates ensembles by selecting high-fitness models based on **calibration data** (see [*Helpers*](helpers.md)). Some calibration nodes may correspond to **input nodes**, which are unconstrained in Boolean logic.

To address this, Bless:

- introduces an **artificial regulator node** that activates or inhibits the input node,
- filters stable states to retain only those **matching the calibration data**.

This ensures consistency between experimental evidence and the states evaluated during downstream analyses.
