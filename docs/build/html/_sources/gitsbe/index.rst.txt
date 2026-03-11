.. _gitsbe-home:

Gitsbe
======

**Gitsbe** — *Generic Interactions To Specific Boolean Equations* — is a Java-based module that generates cell-line-specific Boolean model ensembles. Starting from a general signalling topology and cell-line-calibrated activity profiles (produced by :ref:`Celios <celios-home>`), Gitsbe uses a genetic algorithm to parameterise logic rules so that the resulting models reproduce observed steady-state behaviour.

Each ensemble captures the diversity of Boolean rule sets compatible with the experimental data and serves as input for downstream perturbation analysis with :ref:`Oris <oris-home>`.

.. toctree::
   :maxdepth: 2
   :hidden:

   Overview <self>
   Installation <installation>
   Usage <usage>

.. note::

   Gitsbe is a **Java** application maintained as part of the `DrugLogics <https://github.com/druglogics>`_ project.
   Full API documentation is available at `druglogics.github.io <https://druglogics.github.io/druglogics-doc/gitsbe.html>`_.

----

.. raw:: html

   <p style="font-size:0.75rem;color:#999;margin-top:1rem;">Developed by J. Zobolas</p>