.. _drexpa-home:

Drexpa
======

**Drexpa** — *DRug EXperimental PAnel* — transforms experimental drug screening datasets into *in silico* drug panels and perturbations that can be tested in Boolean models using the TRAFIKK pipeline. It automates drug name resolution, target retrieval, node mapping, and creates drug panels and perturbation files compatible with *in silico* validation workflows.

Pipeline overview
-----------------

.. code-block:: text

   Drug Names (TXT)
     ↓ [chembl_ids]
   ChEMBL IDs
     ↓ [targets]
   Drug Targets (from internal DB)
     ↓ [node_targets] + Node Dict (CSV)
   Logical Model Nodes
     ↓ [profiles]
   Drug Profiles (with Pipeline IDs)
     ├→ [panel] → Drug Panel (DrugLogics format)
     └→ [combinations] + Synergy Data (CSV, optional)
        ↓ [perturbations]
        Perturbation Files (per tissue/cell line)
        ↓ [synergies]
        Synergy Summaries

Pipeline modes
--------------

Drexpa automatically adapts to three execution modes:

1. **No Synergy Data**: Generates drug profiles and panel; skips doses/combinations/synergies.
2. **With Concentration Data**: Full pipeline including dose-based target extraction and combinations.
3. **Without Concentration Data**: Profiles and panel from single-dose targets; combinations from profile mapping.

.. toctree::
   :maxdepth: 2
   :hidden:

   Overview <self>
   Installation <installation>
   Usage <usage>
   Configuration <configuration>