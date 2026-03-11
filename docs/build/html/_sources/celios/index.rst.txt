.. _celios-home:

Celios
======

**Celios** — *CEll LIne OmicS processor* — extracts and integrates multi-omics data into activity datasets from which calibration files can be created for Boolean models used in the TRAFIKK pipeline.

Celios is a configuration-driven two-step pipeline:

1. 🧬 **Node Extraction** — Extract nodes from a biological network (SIF format) and map them to standardised gene symbols (HGNC).
2. 📊 **Activity Calculation** — Integrate multi-omics data (mutations, CNV, TF activity, gene expression) into activity matrices by cell line.

Each step can be skipped or customised via configuration. The pipeline is entirely controlled via JSON or YAML configuration files, making it easy to reproduce analyses and scale to multiple datasets.

.. toctree::
   :maxdepth: 2
   :hidden:

   Overview <self>
   Installation <installation>
   Usage <usage>
   Configuration <configuration>