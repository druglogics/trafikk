# Oris Modes

Oris can operate in three distinct modes, selectable via the `--mode` parameter:

1. **Synergy Mode**
2. **Count Paths Mode**
3. **Full Mode**

---

### 1. Synergy Mode

The **Synergy Mode** is invoked with `--mode synergy `and is used to compute **Bliss synergy excess** for pairs of perturbations, mimicking double-drug treatments.

To perform these computations, Oris relies on several directories and files obtained within the input ZIP archive.

- 📁 **{ref}`Gitsbe <gitsbe-home>`-generated model ensemble**
  - Full ensemble (if no sampling): `src/Models`
  - Sampled ensemble (if sampling enabled): `src/SampledModels`
- 📃 **Calibration data:** `src/training`
- 📃 **{ref}`Drexpa <drexpa-home>`-generated perturbations:** `src/perturbations`
- **📃 {ref}`Drexpa <drexpa-home>`-generated drugpanel:** `src/drugpanel`
- 📃 **Model outputs:** `src/modeloutputs`

The simulation begins by applying **initial conditions** (see [*Initial Conditions*](initialconditions.md)), which constrain the models according to the culture medium and filter stable states that comply with the input-node assignments present in the calibration data.

Next, models undergo **sampling**, selecting only those that complete simulations within the user-defined performance threshold (as configured via the `--sampling` parameter). Once the sampled ensemble is established, Oris reads the perturbation file to generate the perturbed models using [BooLEVARD](https://github.com/farinasm/boolevard)'s `Pert` method. For each defined double perturbation, Oris creates:

- the **double-perturbed model**, and
- the corresponding **single-perturbed models**, whenever one perturbation in the pair appears in at least one double combination.

After assembling the collection of **unperturbed**, **single-perturbed**, and **double-perturbed** models, Oris executes BooLEVARD's `CountPaths` method on all of them to quantify signal transduction toward the nodes listed in the **model outputs file**, and using the information in the `perturbations` and `drugpanel` files.

> 📝 Nodes in the model output file serve as proxies for cell viability.

After simulation, the path-counting results are stored in `Results/PathCounts.txt` inside the analyzed ZIP file. This file is formatted as a dataframe, where each row corresponds to a stable state of a model instance. For each entry, Oris reports:

- the model identifier (model name + perturbation label),
- the stable state evaluated,
- the path counts for all model-output nodes, and
- the local Boolean states of those output nodes.

#### Bliss Synergy Scoring

The final stage consists of computing Bliss synergy scores. To enable this, a **viability score** is first derived from the path counts via a hyperbolic tangent transformation that maps values to the interval $[0, 1]$. Specifically, viability is defined as:

$$
V = \frac{1}{2} \left[ \tanh\!\left( \frac{\sum_{i \in P} p_i - \sum_{j \in N} p_j}{s} \right) + 1 \right]
$$

where:

- $P$ is the set of pro-survival nodes,
- $N$ is the set of pro-death nodes,
- $p_i$ and $p_j$ denote their respective path counts, and
- $s$ is a scaling parameter that controls the compression of viability scores.

In practice, the parameter $s$ is chosen to maximize the dispersion of the viability scores, ensuring an effective spread across the $[0, 1]$ interval. Viability values are then capped at the corresponding unperturbed condition and normalized by it, ensuring that the unperturbed condition attains a value of $V = 1$.

Finally, Bliss synergy scores are calculated as:

$$
E_{\mathrm{Bliss}} = V_{AB} - V_{A}V_{B}
$$

where $V_{AB}$ denotes the viability under the combined perturbation, and $V_{A}$ and $V_{B}$ correspond to the respective single-perturbation conditions.

Synergy excess values are stored in `Results/SynergyExcess.txt`, which contains a dataframe listing each perturbation pair together with its corresponding Bliss synergy excess score.

---

### 2. Count Paths Mode

The **Count Paths Mode** is invoked with `--mode countpaths` and is used to quantify signal propagation across the entire Boolean model by computing path counts toward **every node**, rather than only model output nodes. This mode is useful for exploring how perturbations reshape the internal signaling landscape of the model.

To perform these computations, Oris reads the necessary data from the input ZIP archive:

- 📁 **{ref}`Gitsbe <gitsbe-home>`-generated model ensemble**
  - Full ensemble (if no sampling): `src/Models`
  - Sampled ensemble (if sampling enabled): `src/SampledModels`
- 📃 **Calibration data:** `src/training`
- 📃 **{ref}`Drexpa <drexpa-home>`-generated perturbations:** `src/perturbations`
- **📃 {ref}`Drexpa <drexpa-home>`-generated drugpanel:** `src/drugpanel`

As in other modes, initial conditions are applied (see [*Initial Conditions*](initialconditions.md)) and, if enabled, model sampling is performed according the `--sampling` parameter. Perturbations are then introduced using [BooLEVARD](https://github.com/farinasm/boolevard)'s `Pert` method, generating the corresponding **single** and **double** perturbation models using the information in the `perturbations` and `drugpanel` files.

Once all model instances are prepared, Oris executes BooLEVARD's  `CountPaths` method on each of them, computing path counts toward **all Boolean nodes**, providing a detailed view of signal flow under each perturbation condition.

Simulation results are stored in `Results/PathCountsFull.txt` within the ZIP archive. The file is formatted as a dataframe, where each row corresponds to a stable state of a model instance and contains:

- the model identifier (model name + perturbation label),
- the evaluated stable state,
- the path counts for all Boolean nodes, and
- the Boolean activation states of those nodes.

---

### 3. Full Mode

The **Full Mode** is invoked with `--mode full` and performs both operations provided by the `synergy` and `countpaths` modes in a single execution. In practice, Oris computes:

1. **Bliss synergy excess**, based on viability values derived from model outputs, and
2. **global signal propagation**, via path counting toward all Boolean nodes.

This mode is useful when both internal signaling changes and drug combination effects are of interest.

All intermediate steps (initial conditions, optional sampling, and perturbation generation) follow the same procedure described for the other modes. The resulting output files are writen to the `Results`directory within the input ZIP archive and include:

- `PathCounts.txt` (path counts toward output nodes),
- `SynegyExcess.txt` (Bliss synergy excess values), and
- `PathCountsFull.txt` (path counts toward all Boolean nodes).
