"""
Root package for the Deep Twin Network replication project.

This package contains simple, modular components for
experimenting with the estimation of categorical counterfactuals and
probabilities of causation using an accessible subset of the ideas
introduced in the paper **“Estimating Categorical Counterfactuals via
Deep Twin Networks”** by Vlontzos et al. (2023)【671066552242396†L160-L169】.

The goal of this package is two‑fold:

1. **Provide a reproducible baseline** that mirrors the overall
   experimental pipeline described in the paper, including synthetic
   dataset generation, model training, evaluation of factual and
   counterfactual predictions and estimation of probabilities of
   causation (necessity, sufficiency and necessity & sufficiency).

2. **Offer an extensible framework** where different modelling
   strategies can be plugged in.  While the original work relies on
   TensorFlow Lattice layers to enforce monotonicity, this package
   implements a lightweight logistic–regression‑based strategy by
   default.  Developers can add their own strategies (e.g. deep
   neural networks, monotonic models) by subclassing
   :class:`dtn_repl.models.BaseTwinModel`.

The package is self contained and depends only on `numpy`, `pandas`
and `scikit‑learn`, which are readily available in the execution
environment.

See the module docstrings and the README in the project root for
guidance on usage.
"""

from .datasets import SyntheticDataset, TwinDataset, KenyanDataset, load_dataset
from .models import BaseTwinModel, LogisticTwinModel
from .train import Trainer
from .probcause import ProbabilityOfCausation

__all__ = [
    "SyntheticDataset",
    "TwinDataset",
    "KenyanDataset",
    "load_dataset",
    "BaseTwinModel",
    "LogisticTwinModel",
    "Trainer",
    "ProbabilityOfCausation",
]