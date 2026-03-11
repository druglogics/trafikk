# Helpers

In order to generate Oris input files, the `zipero` plugin is used as follows:

> **TODO:** This section is provided by Viviam.
>
> _Instructions, usage examples, and ZIP generation details should be placed here._

---

Once generated, the resulting file is a ZIP archive containing all the information required to run Oris in any of its modes. The internal directory structure is as follows:

- **`Models/`**
  Contains the {ref}`Gitsbe <gitsbe-home>`-generated Boolean models in **BNET** format.
- **`src/`**
  Contains auxiliary files used throughout the Oris pipeline:
  - **`drugpanel`**
    Defines drug identifiers, modes of action, and target nodes. Used to generate perturbed model instances (see [*Oris Modes*](orismodes.md)).
  - **`training`**
    Calibration data used by {ref}`Gitsbe <gitsbe-home>` to fit Boolean models to experimental profiles. Used in Oris to incorporate initial conditions (see [*Initial Conditions*](initialconditions.md)).
  - **`modeloutputs`**
    Specifies the nodes used as **viability proxies** and assigns them weights:

    - `+1` for pro-survival / positive regulators.
    - `-1` for pro-death / negative regulators.

    Required in the `synergy` and `full` modes (see [*Oris Modes*](orismodes.md)).
  - **`perturbations`**
    Defines the set of **single** and **double** perturbations to be simulated. Used across all modes (see [*Oris Modes*](orismodes.md)).
