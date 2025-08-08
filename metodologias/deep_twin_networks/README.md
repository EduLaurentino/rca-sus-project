# Deep Twin Network Replication

This sub‑directory contains a lightweight, self‑contained replication of the
experimental pipeline described in **“Estimating Categorical
Counterfactuals via Deep Twin Networks”** by Vlontzos et al.  The
original paper introduces deep twin networks with lattice layers to
enforce monotonicity; this implementation provides an accessible
baseline using only `numpy`, `pandas` and `scikit‑learn` while retaining
the overall workflow and terminology.  See the top‑level
README for a description of the broader Ph.D. project and data sources.

## Contents

* `dtn_repl/` – Python package implementing dataset loaders, twin
  models and training utilities.  The synthetic dataset generator
  reproduces the causal mechanism from the paper; loaders for the
  Twins and Kenyan datasets are included (the Kenyan loader is a
  placeholder requiring manual download).  The base model uses two
  logistic regressions to estimate factual and counterfactual
  outcomes.  Modular design via the strategy pattern allows easy
  substitution of more advanced models.
* `run_experiment.py` – Command‑line script demonstrating how to
  generate a dataset, train the baseline model and compute
  probabilities of causation.
* `requirements.txt` – List of Python dependencies required to run
  this code.

## Usage

1. Navigate to this directory and create a Python virtual environment.
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run an experiment, for example on a synthetic dataset:
   ```bash
   python run_experiment.py --dataset synthetic --n_samples 50000
   ```
4. To use the Twins data set, specify `--dataset twins`.  The loader
   will automatically download the data from the GANITE repository if
   it is not present locally.

## Relation to the Original Paper

The original work uses TensorFlow Lattice to learn causal mechanisms
under counterfactual ordering constraints.  Our baseline does not
enforce monotonicity but illustrates how to build and evaluate twin
models with the available tools.  Probabilities of causation (PN,
PS and PNS) are computed following the definitions discussed in
Tian and Pearl’s work and adopted in the paper【671066552242396†L162-L169】.
