"""
Model definitions for Deep Twin Network replication.

The original deep twin network employs lattice models with monotonicity
constraints to learn causal mechanisms consistent with counterfactual
ordering【671066552242396†L160-L169】.  In this replication we aim to
provide an extensible base class and a simple baseline implementation
using logistic regression.  Additional strategies can be implemented
by subclassing :class:`BaseTwinModel` and overriding the
``fit`` and ``predict_proba`` methods.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Tuple, Dict, Any

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression


class BaseTwinModel(ABC):
    """Abstract base class for models that predict factual and counterfactual outcomes.

    A twin model takes as input a data frame with at least the columns
    ``X``, ``U_y`` and ``X_prime`` and learns to predict the outcome
    variables ``Y`` (factual) and ``Y_prime`` (counterfactual).  Derived
    classes must implement the ``fit`` and ``predict_proba`` methods.
    """

    def __init__(self, **kwargs: Any) -> None:
        pass

    @abstractmethod
    def fit(self, X: pd.DataFrame, y: pd.DataFrame) -> 'BaseTwinModel':
        """Fit the model on training data.

        Parameters
        ----------
        X : pandas.DataFrame
            Data frame containing columns ``X``, ``U_y``, ``X_prime`` and
            any additional covariates.
        y : pandas.DataFrame
            Data frame with columns ``Y`` and ``Y_prime``.

        Returns
        -------
        BaseTwinModel
            Returns self to allow chaining.
        """

    @abstractmethod
    def predict_proba(self, X: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """Predict factual and counterfactual outcome probabilities.

        Parameters
        ----------
        X : pandas.DataFrame
            Data frame containing columns ``X``, ``U_y``, ``X_prime`` and
            optional covariates.

        Returns
        -------
        (np.ndarray, np.ndarray)
            A tuple of length‐2 arrays ``(p_y, p_y_prime)`` containing
            predicted probabilities for the factual and counterfactual
            outcomes.  Each array must be shaped ``(n_samples,)`` and
            values must lie in ``[0, 1]``.
        """


class LogisticTwinModel(BaseTwinModel):
    """Baseline twin model using logistic regression.

    This model fits two independent logistic regressions: one for the
    factual outcome ``Y`` given features ``(X, U_y)`` and one for the
    counterfactual outcome ``Y_prime`` given ``(X_prime, U_y)``.

    Although this differs from the lattice architecture in the
    original paper, it preserves the core idea of estimating
    probabilities for both factual and counterfactual outcomes based
    on the same latent information.  It also demonstrates how to use
    the strategy pattern: other models can be implemented by
    subclassing :class:`BaseTwinModel` and replacing the two logistic
    regressions with alternative estimators.
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        # separate models for Y and Y'
        self.model_y = LogisticRegression(max_iter=500)
        self.model_y_prime = LogisticRegression(max_iter=500)

    def fit(self, X: pd.DataFrame, y: pd.DataFrame) -> 'LogisticTwinModel':
        # prepare feature matrices
        X_factual = X[['X', 'U_y']].to_numpy()
        X_counter = X[['X_prime', 'U_y']].to_numpy()
        # extract targets
        y_factual = y['Y'].astype(int).to_numpy()
        y_counter = y['Y_prime'].astype(int).to_numpy()
        # fit logistic models
        self.model_y.fit(X_factual, y_factual)
        self.model_y_prime.fit(X_counter, y_counter)
        return self

    def predict_proba(self, X: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        X_factual = X[['X', 'U_y']].to_numpy()
        X_counter = X[['X_prime', 'U_y']].to_numpy()
        p_y = self.model_y.predict_proba(X_factual)[:, 1]
        p_y_prime = self.model_y_prime.predict_proba(X_counter)[:, 1]
        return p_y, p_y_prime
