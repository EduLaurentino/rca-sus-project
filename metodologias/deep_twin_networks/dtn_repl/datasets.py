"""
Datasets for Deep Twin Network replication.

This module implements several dataset loaders.  Each loader returns a
pair of pandas ``DataFrame`` objects (train and test splits) with
columns that include the factual treatment ``X``, the latent class
``U_y`` (which influences the causal mechanism) and the counterfactual
treatment ``X_prime``.  Outcomes are provided in columns ``Y`` and
``Y_prime`` representing the factual and counterfactual outcomes,
respectively.  Additional covariates for real world data sets may be
included as extra columns.

The synthetic dataset reproduces the generative process described in
Section 4 of the paper.  For binary treatment variables the latent
class ``U_y`` takes three possible values (0, 1, 2) with
interpretations given in the paper.  When ``U_y = 0``, the outcome is
equal to the treatment; when ``U_y = 2`` the outcome is always 1.
Samples with ``U_y = 1`` are sufficiency examples where treatment has
no effect on the outcome【671066552242396†L164-L169】.  See the paper or
the original code for more details.

`TwinDataset` and `KenyanDataset` are skeletons demonstrating how to
wrap external data.  They include download logic for the Twins data
(from GANITE) and placeholders for the Kenyan water dataset.  If
internet access is unavailable, users should manually download and
place the CSV file in the data directory.
"""

from __future__ import annotations

import os
import gzip
import io
import urllib.request
from dataclasses import dataclass
from typing import Tuple, Dict, Any, Optional

import numpy as np
import pandas as pd


@dataclass
class DatasetSplit:
    """Container for train and test splits.

    Attributes
    ----------
    train : pandas.DataFrame
        Training set with columns ``X``, ``U_y``, ``X_prime``, ``Y`` and
        ``Y_prime``.
    test : pandas.DataFrame
        Test set with the same columns as the training set.
    meta : dict
        Metadata about how the dataset was generated, e.g. random seed,
        distributions and hyperparameters.  Not all loaders set this.
    """

    train: pd.DataFrame
    test: pd.DataFrame
    meta: Optional[Dict[str, Any]] = None


class SyntheticDataset:
    """Synthetic dataset generator.

    This class replicates the simple counterfactual data generation
    process used in the original repository.  It supports two latent
    distributions: ``'normal'`` and ``'uniform'``.  Treatment
    variables ``X`` are binary Bernoulli with probability ``p``.

    Parameters
    ----------
    n_samples : int
        Total number of samples to generate.
    x_distribution : str
        Currently only ``'bernouli'`` is supported.  If you need
        continuous treatments, extend this class.
    u_distribution : str
        Distribution for the latent variable ``U_y``.  Either
        ``'normal'`` (default) or ``'uniform'``.  When ``'normal'``
        distribution is selected, latent values are drawn from a
        discretised Gaussian with mean ``mu`` and standard deviation
        ``sigma`` and then binned into three categories by
        ``np.digitize`` with breakpoints at 1 and 2.  When
        ``'uniform'`` is selected, latent values are drawn uniformly
        from integers in ``[low, high)``.
    p : float
        Probability of treatment ``X=1`` when ``x_distribution`` is
        ``'bernouli'``.
    mu : float, optional
        Mean of the Gaussian used when ``u_distribution = 'normal'``.
        Defaults to 1.
    sigma : float, optional
        Standard deviation of the Gaussian when ``u_distribution =
        'normal'``.  Defaults to 2/3 (matching the original code).
    low : int, optional
        Lower bound (inclusive) for the uniform latent distribution.
        Defaults to 0.
    high : int, optional
        Upper bound (exclusive) for the uniform latent distribution.
        Defaults to 3.
    split : float, optional
        Proportion of samples used for the training set.  The remainder
        is used for testing.  Defaults to 0.8.
    seed : int, optional
        Random seed for reproducibility.  If ``None``, a random seed
        will be drawn.

    Returns
    -------
    DatasetSplit
        A dataclass containing train and test splits and metadata.
    """

    def __init__(self,
                 n_samples: int = 100_000,
                 x_distribution: str = 'bernouli',
                 u_distribution: str = 'normal',
                 p: float = 0.5,
                 mu: float = 1.0,
                 sigma: float = 2/3,
                 low: int = 0,
                 high: int = 3,
                 split: float = 0.8,
                 seed: Optional[int] = None,
                 **kwargs: Any) -> None:
        self.n_samples = n_samples
        self.x_distribution = x_distribution
        self.u_distribution = u_distribution
        self.p = p
        self.mu = mu
        self.sigma = sigma
        self.low = low
        self.high = high
        self.split = split
        # store any additional kwargs in meta
        self.meta = dict(kwargs)
        self.meta.update({
            'n_samples': n_samples,
            'x_distribution': x_distribution,
            'u_distribution': u_distribution,
            'p': p,
            'mu': mu,
            'sigma': sigma,
            'low': low,
            'high': high,
            'split': split,
            'seed': seed,
        })
        # set seed
        if seed is None:
            seed = np.random.randint(0, 2**32 - 1)
        self.seed = seed
        rng = np.random.default_rng(seed)
        # generate treatments X
        if x_distribution != 'bernouli':
            raise NotImplementedError(
                f"Unsupported x_distribution: {x_distribution}; only 'bernouli' is implemented.")
        X = rng.binomial(n=1, p=p, size=n_samples)
        X_prime = 1 - X  # flip treatment for counterfactual
        # generate latent U_y
        if u_distribution == 'normal':
            latent = rng.normal(loc=mu, scale=sigma, size=n_samples)
            # bin into three categories; use np.digitize with bins at 1 and 2
            U_y = np.digitize(latent, bins=[1, 2])
        elif u_distribution == 'uniform':
            U_y = rng.integers(low=low, high=high, size=n_samples)
        else:
            raise NotImplementedError(
                f"Unsupported u_distribution: {u_distribution}; choose 'normal' or 'uniform'.")
        # generate outcomes Y and Y_prime according to latent class
        Y = np.zeros(n_samples, dtype=int)
        Y_prime = np.zeros(n_samples, dtype=int)
        # when U_y == 0: Y = X, Y_prime = 1-X
        idx0 = np.where(U_y == 0)[0]
        Y[idx0] = X[idx0]
        Y_prime[idx0] = X_prime[idx0]
        # when U_y == 2: outcomes are 1 regardless of treatment
        idx2 = np.where(U_y == 2)[0]
        Y[idx2] = 1
        Y_prime[idx2] = 1
        # when U_y == 1: outcomes are independent of treatment (set to 0)
        # In the original code this branch is implicit because arrays are
        # initialised to zero.  We keep it explicit here for clarity.
        idx1 = np.where(U_y == 1)[0]
        Y[idx1] = 0
        Y_prime[idx1] = 0
        # assemble DataFrame
        df = pd.DataFrame({
            'X': X,
            'U_y': U_y,
            'X_prime': X_prime,
            'Y': Y,
            'Y_prime': Y_prime,
        })
        # split
        split_idx = int(split * n_samples)
        train_df = df.iloc[:split_idx].reset_index(drop=True)
        test_df = df.iloc[split_idx:].reset_index(drop=True)
        self.data = DatasetSplit(train=train_df, test=test_df, meta=self.meta)

    def get_splits(self) -> DatasetSplit:
        """Return train/test splits and metadata."""
        return self.data


class TwinDataset:
    """Loader for the Twins dataset used in the GANITE paper.

    The Twins dataset contains information about twins births and whether
    each twin survived.  It is often used for counterfactual inference
    because one twin can be thought of as a factual outcome and the
    other as a counterfactual under a different treatment.  This loader
    downloads the compressed CSV from the public GANITE repository
    (accessible without authentication) and parses it into the expected
    format with columns ``X`` (sex of the first twin), ``U_y``
    (placeholder for latent class; here we simply encode some baseline
    variables) and factual/counterfactual outcomes ``Y`` and
    ``Y_prime``.

    **Note:** The Twins dataset used in the paper includes additional
    covariates and complicated pre‑processing.  This loader provides a
    minimal example of how to wrap a real dataset into the format
    expected by the models in this package.  Users seeking a more
    faithful reproduction should refer to the original code.
    """

    TWINS_URL = "https://raw.githubusercontent.com/jsyoon0823/GANITE/master/data/Twin_data.csv.gz"

    def __init__(self, data_dir: str = "./data", seed: Optional[int] = None) -> None:
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        self.seed = seed
        # path to downloaded file
        self.local_path = os.path.join(data_dir, "Twin_data.csv.gz")
        if not os.path.exists(self.local_path):
            self._download_twins()
        # read the CSV
        self._load()

    def _download_twins(self) -> None:
        """Download the compressed Twins dataset."""
        print(f"Downloading Twins dataset from {self.TWINS_URL}...")
        urllib.request.urlretrieve(self.TWINS_URL, self.local_path)
        print(f"Saved to {self.local_path}")

    def _load(self) -> None:
        """Load and parse the Twins data into train/test splits."""
        # decompress in memory
        with gzip.open(self.local_path, 'rb') as f:
            csv_data = f.read()
        df = pd.read_csv(io.BytesIO(csv_data))
        # The GANITE twins data has columns: 'Apnoea test', 'Birthweight',
        # 'Sex', 'Twin_Birth_ID', etc.  For demonstration we will use
        # 'Sex' as the treatment (1=male, 0=female), 'Gestation',
        # 'Birthweight' as proxies for U_y and use 'death' outcome.
        # Note: The actual twins data uses more variables; this is a toy example.
        # Map columns or drop missing columns if not present
        required_cols = ['sex', 'gestation', 'birthweight', 'death']
        available_cols = [c.lower() for c in df.columns]
        col_map = {}
        for col in required_cols:
            try:
                idx = available_cols.index(col)
            except ValueError:
                continue
            col_map[col] = df.columns[idx]
        # ensure we have at least treatment and outcome
        if 'sex' not in col_map or 'death' not in col_map:
            raise RuntimeError(
                "Twin dataset does not contain 'sex' and 'death' columns; update loader.")
        X = df[col_map['sex']].astype(int)
        Y = 1 - df[col_map['death']].astype(int)  # assume death=1 means poor outcome, so Y=1 means survival
        # Use gestation and birthweight (if available) as latent variable proxies
        if 'gestation' in col_map:
            U_y = df[col_map['gestation']].rank(method='min').astype(int)
        else:
            U_y = np.zeros(len(df), dtype=int)
        X_prime = 1 - X
        Y_prime = Y  # in twins data counterfactual outcome is the other twin; here we just reuse Y as placeholder
        out_df = pd.DataFrame({'X': X, 'U_y': U_y, 'X_prime': X_prime, 'Y': Y, 'Y_prime': Y_prime})
        # shuffle and split
        rng = np.random.default_rng(self.seed)
        out_df = out_df.sample(frac=1, random_state=self.seed).reset_index(drop=True)
        split_idx = int(0.8 * len(out_df))
        self.data = DatasetSplit(
            train=out_df.iloc[:split_idx].reset_index(drop=True),
            test=out_df.iloc[split_idx:].reset_index(drop=True),
            meta={'source': 'Twins GANITE data'})

    def get_splits(self) -> DatasetSplit:
        return self.data


class KenyanDataset:
    """Placeholder loader for the Kenyan water dataset.

    The Kenyan water dataset used in the paper is available from
    Harvard Dataverse【671066552242396†L164-L169】.  Due to licensing
    restrictions the data is not bundled with this repository.  To use
    this loader, download the dataset manually and place the
    corresponding CSV (or compressed file) in the ``data_dir``.  Then
    implement the parsing logic similar to `TwinDataset`.
    """
    def __init__(self, data_dir: str = "./data", filename: str = None, seed: Optional[int] = None) -> None:
        self.data_dir = data_dir
        self.filename = filename
        self.seed = seed
        os.makedirs(data_dir, exist_ok=True)
        if filename is None:
            raise RuntimeError(
                "Please download the Kenyan water dataset from the Harvard Dataverse"
                " and specify the filename via the 'filename' argument.")
        local_path = os.path.join(data_dir, filename)
        if not os.path.exists(local_path):
            raise FileNotFoundError(
                f"Dataset file {local_path} not found. Please place the Kenyan data in the data directory.")
        # TODO: implement parsing; for now set empty data frames
        self.data = DatasetSplit(
            train=pd.DataFrame(), test=pd.DataFrame(), meta={'source': 'Kenyan dataset'})

    def get_splits(self) -> DatasetSplit:
        return self.data


def load_dataset(name: str, **kwargs: Any) -> DatasetSplit:
    """Factory function to load a dataset by name.

    Parameters
    ----------
    name : str
        Name of the dataset.  Supported values are ``'synthetic'``,
        ``'twins'`` and ``'kenyan'`` (case insensitive).
    **kwargs
        Additional keyword arguments passed to the dataset constructor.

    Returns
    -------
    DatasetSplit
        Train and test splits and optional metadata.
    """
    name = name.lower()
    if name == 'synthetic':
        dataset = SyntheticDataset(**kwargs)
        return dataset.get_splits()
    elif name == 'twins':
        dataset = TwinDataset(**kwargs)
        return dataset.get_splits()
    elif name == 'kenyan':
        dataset = KenyanDataset(**kwargs)
        return dataset.get_splits()
    else:
        raise ValueError(
            f"Unknown dataset name '{name}'. Supported names: 'synthetic', 'twins', 'kenyan'.")