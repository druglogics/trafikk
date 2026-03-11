# Usage

## 📝 Overview

Gitsbe takes a general Boolean network topology together with cell-line-specific training data (produced by [Celios](../celios/index.rst)) and evolves an ensemble of Boolean models whose attractors match observed steady-state behaviour.

The genetic algorithm explores the space of possible logic rules for each node in the network, selecting those parameterisations that best reproduce the training profile.

## 🔄 Workflow within TRAFIKK

1. 📥 **Input**: General signalling network (`.sif`) + cell-line training data from [Celios](../celios/index.rst)
2. ⚙️ **Process**: Genetic-algorithm-based model parameterisation
3. 📦 **Output**: Ensemble of Boolean models (`.zip`) used by [Oris](../oris/index.rst)

## ⚙️ Configuration

Gitsbe is configured via property files that control the genetic algorithm parameters (population size, mutation rate, number of generations, etc.) and input/output paths.

For detailed configuration options and usage examples, see the [Gitsbe documentation](https://druglogics.github.io/druglogics-doc/gitsbe.html).

## 🔗 Source code

The source code is available at [github.com/druglogics/gitsbe](https://github.com/druglogics/gitsbe).
