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

* `dtn_repl/` – Python package implementing dataset loaders,
  twin models and training utilities.  The synthetic dataset
  generator reproduces the causal mechanism from the paper;
  loaders for the Twins and Kenyan datasets are included (the
  Kenyan loader is a placeholder requiring manual download).  The
  package defines an abstract `BaseTwinModel` and several
  concrete strategies:

  * `LogisticTwinModel` (baseline) – requires both factual and
    counterfactual outcomes and is intended for synthetic data;

  * `SLearnerTwinModel` – implements a single‑model (S‑learner)
    meta‑learner using a gradient boosting classifier.  It trains
    one model on the factual outcome and uses the trained model to
    predict potential outcomes under treatment and control by
    toggling the treatment variable.  This strategy does *not*
    require counterfactual labels and therefore supports
    observational data;

  * `TLearnerTwinModel` – implements a two‑model (T‑learner)
    meta‑learner using random forests.  Separate models are
    trained on treated and control subsets to estimate potential
    outcomes.  Like the S‑learner, it only needs the factual
    outcome and is suited to observational data.

  * `XLearnerTwinModel` – implements an X‑learner, a more advanced
    meta‑learning strategy that estimates heterogeneous treatment
    effects.  It first fits T‑learner outcome models, then imputes
    treatment effects and trains regressors to predict those
    effects.  The imputed effects are combined to compute the
    potential outcomes under both treatment and control.  This
    approach only requires factual outcomes and supports
    observational data.

  The design follows the strategy pattern, making it easy to plug in
  alternative models such as causal forests or neural networks when
  additional libraries become available.
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
3. Run an experiment.  For synthetic data with both factual and
   counterfactual labels you can use the logistic baseline:

   ```bash
   python run_experiment.py --dataset synthetic --n_samples 50000 --model logistic
   ```

   For observational data (e.g., the Twins dataset) where only the
   factual outcome is observed, choose either the S‑learner, T‑learner
   or X‑learner strategy:

   ```bash
   # S‑learner on Twins data
   python run_experiment.py --dataset twins --model slearner

   # T‑learner on Twins data
   python run_experiment.py --dataset twins --model tlearner

    # X‑learner on Twins data
    python run_experiment.py --dataset twins --model xlearner
   ```

4. The loader will automatically download the Twins data from the
   GANITE repository if it is not present locally.  For the Kenyan
   dataset you must download the data manually; see the documentation
   in `dtn_repl/datasets.py`.

## Relation to the Original Paper

The original work uses TensorFlow Lattice to learn causal mechanisms
under counterfactual ordering constraints.  Our baseline does not
enforce monotonicity but illustrates how to build and evaluate twin
models with the available tools.  Probabilities of causation (PN,
PS and PNS) are computed following the definitions discussed in
Tian and Pearl’s work and adopted in the paper【671066552242396†L162-L169】.
