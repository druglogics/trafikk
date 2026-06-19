# SIF Inspector Before Running Gitsbe

## Purpose

Before generating Boolean model ensembles with Gitsbe, users can run `sif_inspector.py` to inspect the source SIF network.

This script helps identify:

- candidate input nodes
- candidate output nodes
- internal nodes
- self-loops
- conflicting regulatory edges

This is useful because new users may not know which nodes should be used as model outputs for Gitsbe or as `media_targets` later in the Oris configuration.

The script does not modify the network. It only summarizes the structure of the SIF file and highlights potential issues that should be reviewed before running Gitsbe.

---

## When to use this script

Run this script after preparing the SIF network and before running Gitsbe.

Recommended workflow:

```text
SIF network
-> sif_inspector.py
-> review candidate inputs/outputs
-> define modeloutputs for Gitsbe
-> run Gitsbe
-> create Oris ZIP inputs
-> run Oris Boolean rule preflight
-> run Oris
```

---

## Input format

The script expects a SIF file with no header.

Each line should contain three tab-separated columns:

```text
source    interaction    target
```

Example:

```text
EGFR    ->    MTOR
FBXW7   -|    SIGNOR_PF30
```

Supported interactions:

```text
->    activation
-|    inhibition
```

Empty lines and comment lines starting with `#` are ignored.

---

## Running the script

Run:

```bash
python sif_inspector.py network.sif --out sif_inspection
```

If no output folder is provided, the script writes results to:

```text
sif_inspection/
```

---

## What the script checks

### Candidate input nodes

Candidate input nodes are nodes with outgoing edges but no incoming edges.

In graph terms:

```text
candidate_inputs = sources - targets
```

These nodes are potential candidates for the `media_targets` parameter in the Oris configuration.

Example:

```text
A -> B
C -| B
B -> D
```

Sources:

```text
A, C, B
```

Targets:

```text
B, D
```

Candidate inputs:

```text
A, C
```

These nodes regulate the network but are not regulated by other nodes in the SIF.

---

### Candidate output nodes

Candidate output nodes are nodes with incoming edges but no outgoing edges.

In graph terms:

```text
candidate_outputs = targets - sources
```

These nodes are potential candidates for the `modeloutputs` file used by Gitsbe.

Example:

```text
A -> B
B -> D
```

Sources:

```text
A, B
```

Targets:

```text
B, D
```

Candidate outputs:

```text
D
```

This means `D` is regulated by the network but does not regulate any other node in the SIF.

---

### Internal nodes

Internal nodes are nodes that appear both as source and target.

In graph terms:

```text
internal_nodes = sources ∩ targets
```

These nodes both receive regulation and regulate other nodes.

---

### Self-loops

A self-loop occurs when a node regulates itself.

Example:

```text
SIGNOR_C156 -> SIGNOR_C156
```

or:

```text
SIGNOR_C156 -| SIGNOR_C156
```

Self-loops are not always wrong, but they should be reviewed because they can strongly affect Boolean model behavior.

---

### Conflicting regulatory edges

A conflicting regulatory edge occurs when the same source-target pair has both activation and inhibition.

Example:

```text
SIGNOR_C156 -> SIGNOR_C156
SIGNOR_C156 -| SIGNOR_C156
```

This means the same node is represented as both activating and inhibiting the same target.

This can cause problems during Boolean rule generation. For example, if the conflicting regulation is converted into the rule:

```text
SIGNOR_C156 | !SIGNOR_C156
```

the expression simplifies to:

```text
1
```

meaning the node is always ON.

This type of issue should be resolved before running Gitsbe.

---

## Output files

The script creates several CSV files.

### `sif_candidate_inputs.csv`

Lists candidate input nodes.

Columns:

```text
node
n_outgoing
```

These nodes may be useful when defining `media_targets` in the Oris configuration.

---

### `sif_candidate_outputs.csv`

Lists candidate output nodes.

Columns:

```text
node
n_incoming
```

These nodes may be useful when defining the `modeloutputs` file for Gitsbe.

---

### `sif_internal_nodes.csv`

Lists nodes that are both regulated and regulators.

Columns:

```text
node
n_incoming
n_outgoing
```

---

### `sif_self_loops.csv`

Lists self-regulatory edges.

Columns:

```text
source
interaction
target
```

Example:

```text
SIGNOR_C156,->,SIGNOR_C156
SIGNOR_C156,-|,SIGNOR_C156
```

---

### `sif_conflicting_edges.csv`

Lists source-target pairs that have both activation and inhibition.

Columns:

```text
source
target
has_activation
has_inhibition
issue_type
```

Example:

```text
SIGNOR_C156,SIGNOR_C156,True,True,conflicting_regulation
```

---

### `sif_malformed_lines.csv`

Lists lines that could not be parsed correctly.

Columns:

```text
line_number
line_content
error_message
```

The script continues running even if malformed lines are found.

---

### `sif_summary.csv`

Contains summary metrics.

Example:

```text
metric,value
n_nodes,85
n_edges,230
n_candidate_inputs,12
n_candidate_outputs,5
n_internal_nodes,68
n_self_loops,2
n_conflicting_edges,1
```

---

## Example test network

Example SIF:

```text
A    ->    B
C    -|    B
B    ->    D
E    ->    E
E    -|    E
```

Expected result:

Candidate inputs:

```text
A
C
```

Candidate outputs:

```text
D
```

Internal nodes:

```text
B
E
```

Self-loops:

```text
E -> E
E -| E
```

Conflicting edge:

```text
E to E
```

because `E` both activates and inhibits itself.

---

## How users should interpret the results

The script provides candidates, not final biological decisions.

### Candidate inputs

Candidate input nodes are graph source nodes. These may be good candidates for Oris `media_targets`, but users should review them biologically before using them.

A candidate input may represent:

- receptor activity
- ligand or environmental signal
- drug/media condition
- upstream pathway signal

Not every graph source node is automatically a good media target.

---

### Candidate outputs

Candidate output nodes are graph sink nodes. These may be good candidates for the Gitsbe `modeloutputs` file, but users should review them biologically.

A candidate output may represent:

- phenotype node
- pathway endpoint
- cell fate node
- response marker

Not every graph sink node is automatically a biologically meaningful model output.

---

### Conflicting edges

Conflicting edges should be reviewed carefully before running Gitsbe.

If the same source-target pair appears with both activation and inhibition, Boolean rule generation may create logical contradictions or tautologies.

In the tested Oris/Gitsbe workflow, a conflicting self-loop for `SIGNOR_C156` generated the problematic Boolean rule:

```text
SIGNOR_C156 = EGFR | ERBB3 | IGF1R | KDR | KIT | SIGNOR_C156 | TGFBR1 | !SIGNOR_C156
```

which simplified to:

```text
SIGNOR_C156 = 1
```

This caused most generated Boolean models to fail the later Oris preflight validation.

---

## Recommended workflow for new users

1. Prepare the SIF network.
2. Run `sif_inspector.py`.
3. Review `sif_candidate_inputs.csv`.
4. Decide which nodes should be used as Oris `media_targets`.
5. Review `sif_candidate_outputs.csv`.
6. Decide which nodes should be included in the Gitsbe `modeloutputs` file.
7. Review `sif_self_loops.csv`.
8. Review `sif_conflicting_edges.csv`.
9. Fix problematic SIF edges if needed.
10. Run Gitsbe.
11. Run the Oris Boolean rule preflight script on generated ZIP files.
12. Run Oris.

---

## Important notes

The script should not automatically remove or fix network edges.

Network correction should be done manually because edge signs and self-loops can have biological meaning.

For example, a positive self-loop may represent positive feedback, and a negative self-loop may represent negative feedback. However, having both for the same source-target pair can create ambiguous or invalid Boolean logic.

The safest first action for contradictory self-loops is usually to review the source evidence and decide whether one edge, both edges, or neither edge should remain in the network.

---

## Future improvements

Future versions of the SIF inspector could add:

1. A report of repeated duplicated edges.
2. Detection of unsupported interaction symbols.
3. Optional network visualization.
4. Optional comparison between original and cleaned SIF files.

For now, `sif_inspector.py` provides a lightweight quality-control step before Gitsbe.
