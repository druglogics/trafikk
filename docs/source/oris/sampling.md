# Sampling

Since Oris builds on top of [BooLEVARD](https://github.com/farinasm/boolevard), running full simulations can become computationally expensive when Boolean models are large (≈100 nodes or more) and/or when a large number of perturbations must be evaluated. To mitigate this, Oris implements a sampling procedure in which models are randomly selected and evaluated using BooLEVARD's `CountPaths` method.

Models that complete the simulation within a user-defined time threshold (configured in the [*configuration*](configuration.md) file)  are retained. This process continues until the requested sample size is reached (as defined by the `--sampling` parameter).

If fewer models than requested satisfy the threshold, Oris will still proceed using the available subset.
