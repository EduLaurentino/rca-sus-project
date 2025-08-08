"""
Training utilities for Deep Twin Network replication.

This module defines a :class:`Trainer` class that orchestrates the
end‑to‑end pipeline: loading a dataset, fitting a model, evaluating
factual and counterfactual predictions, computing classification
accuracies and estimating probabilities of causation.

The training logic is deliberately simple to make it clear how to
extend or replace components.  For example, users can swap the
``LogisticTwinModel`` with a more sophisticated model class without
modifying the :class:`Trainer` implementation.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score

from .datasets import DatasetSplit
from .models import BaseTwinModel
from .probcause import compute_probabilities_of_causation, ProbabilityOfCausation


@dataclass
class TrainingResult:
    """Container for training and evaluation results."""
    factual_accuracy: float
    counterfactual_accuracy: float
    prob_causation: ProbabilityOfCausation
    metadata: Dict[str, Any]


class Trainer:
    """Orchestrates training and evaluation of a twin model on a dataset."""

    def __init__(self,
                 model: BaseTwinModel,
                 dataset: DatasetSplit,
                 threshold: float = 0.5) -> None:
        """
        Parameters
        ----------
        model : BaseTwinModel
            The twin model to train.  Must implement ``fit`` and
            ``predict_proba``.
        dataset : DatasetSplit
            Object containing train and test splits.
        threshold : float, optional
            Decision threshold for converting probabilities into binary
            predictions.  Defaults to 0.5.
        """
        self.model = model
        self.dataset = dataset
        self.threshold = threshold

    def run(self) -> TrainingResult:
        """Train the model and evaluate it on the test set.

        Returns
        -------
        TrainingResult
            Object containing accuracy metrics and probabilities of
            causation.
        """
        # prepare training data
        X_train = self.dataset.train[['X', 'U_y', 'X_prime']].copy()
        y_train = self.dataset.train[['Y', 'Y_prime']].copy()
        # fit model
        self.model.fit(X_train, y_train)
        # evaluate on test set
        X_test = self.dataset.test[['X', 'U_y', 'X_prime']].copy()
        y_test = self.dataset.test[['Y', 'Y_prime']].copy()
        p_y, p_y_prime = self.model.predict_proba(X_test)
        # binary predictions
        y_pred = (p_y >= self.threshold).astype(int)
        y_prime_pred = (p_y_prime >= self.threshold).astype(int)
        # compute accuracies
        factual_accuracy = accuracy_score(y_test['Y'].astype(int), y_pred)
        counterfactual_accuracy = accuracy_score(y_test['Y_prime'].astype(int), y_prime_pred)
        # compute probabilities of causation
        prob_causation = compute_probabilities_of_causation(p_y, p_y_prime)
        # compile metadata
        meta = {
            'dataset_meta': self.dataset.meta,
            'model_class': self.model.__class__.__name__,
            'threshold': self.threshold,
        }
        return TrainingResult(
            factual_accuracy=factual_accuracy,
            counterfactual_accuracy=counterfactual_accuracy,
            prob_causation=prob_causation,
            metadata=meta
        )