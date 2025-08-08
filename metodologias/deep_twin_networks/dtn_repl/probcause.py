"""
Estimation of probabilities of causation.

This module provides functions to compute the three probabilities of
causation defined by Tian and Pearl—probability of necessity (PN),
probability of sufficiency (PS) and probability of necessity and
sufficiency (PNS)【671066552242396†L164-L169】—from predicted factual and
counterfactual outcomes.

Given predicted probabilities for the factual outcome (Y) and the
counterfactual outcome (Y'), these quantities are estimated at the
sample level and then averaged over the test set.  The definitions
assume binary outcomes and treatments.

For a single instance ``i`` with factual prediction ``p_y[i]`` and
counterfactual prediction ``p_y_prime[i]``, the estimated PN, PS and
PNS are computed as follows:

``PN[i]  = (1 - p_y_prime[i]) * p_y[i]``
``PS[i]  = (1 - p_y[i]) * p_y_prime[i]``
``PNS[i] = p_y[i] - p_y_prime[i]``

Finally the overall PN, PS and PNS are the means of the instance
values divided by the mean of the factual probabilities (as suggested
in the original code).  See the paper for derivations.
"""

from __future__ import annotations

import numpy as np
from dataclasses import dataclass


@dataclass
class ProbabilityOfCausation:
    """Container for probabilities of causation.

    Attributes
    ----------
    pn : float
        Estimated probability of necessity.
    ps : float
        Estimated probability of sufficiency.
    pns : float
        Estimated probability of necessity and sufficiency.
    """
    pn: float
    ps: float
    pns: float


def compute_probabilities_of_causation(p_y: np.ndarray, p_y_prime: np.ndarray) -> ProbabilityOfCausation:
    """Compute probabilities of causation from predicted outcomes.

    Parameters
    ----------
    p_y : np.ndarray
        Predicted probability of the factual outcome being 1.
    p_y_prime : np.ndarray
        Predicted probability of the counterfactual outcome being 1.

    Returns
    -------
    ProbabilityOfCausation
        Estimated PN, PS and PNS.
    """
    # PN: probability that the treatment is necessary for the outcome
    pn_vals = (1.0 - p_y_prime) * p_y
    # PS: probability that the treatment is sufficient for the outcome
    ps_vals = (1.0 - p_y) * p_y_prime
    # PNS: probability of necessity & sufficiency
    pns_vals = p_y - p_y_prime
    # Normalise by mean factual probability (as in original code)
    mean_p_y = p_y.mean() if p_y.mean() > 0 else 1.0
    pn = pn_vals.mean() / mean_p_y
    ps = ps_vals.mean() / mean_p_y
    pns = pns_vals.mean() / mean_p_y
    return ProbabilityOfCausation(pn=pn, ps=ps, pns=pns)