#!/usr/bin/env python3
"""
Command‑line interface for running experiments with the Deep Twin Network replication.

This script allows users to generate synthetic data, train a simple twin
model and evaluate its performance and probabilities of causation.

Example usage:

```
python run_experiment.py --dataset synthetic --n_samples 50000
```

Use ``--help`` to see all available options.
"""

import argparse
import json
from typing import Any, Dict

from dtn_repl import (
    load_dataset,
    LogisticTwinModel,
    Trainer,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Deep Twin Network replication experiments")
    parser.add_argument('--dataset', type=str, default='synthetic', choices=['synthetic', 'twins', 'kenyan'],
                        help='Dataset to use')
    # synthetic dataset parameters
    parser.add_argument('--n_samples', type=int, default=100000,
                        help='Number of samples for synthetic dataset')
    parser.add_argument('--x_distribution', type=str, default='bernouli', help='Treatment distribution')
    parser.add_argument('--u_distribution', type=str, default='normal', help='Latent variable distribution')
    parser.add_argument('--p', type=float, default=0.5, help='Probability of treatment = 1')
    parser.add_argument('--split', type=float, default=0.8, help='Train/test split fraction')
    parser.add_argument('--seed', type=int, default=42, help='Random seed')
    # model parameters (future extension)
    parser.add_argument('--threshold', type=float, default=0.5, help='Decision threshold for classification')
    return parser.parse_args()


def main(args: argparse.Namespace) -> None:
    # prepare dataset
    if args.dataset == 'synthetic':
        dataset_kwargs: Dict[str, Any] = dict(
            n_samples=args.n_samples,
            x_distribution=args.x_distribution,
            u_distribution=args.u_distribution,
            p=args.p,
            split=args.split,
            seed=args.seed,
        )
    else:
        dataset_kwargs = dict()
    data = load_dataset(args.dataset, **dataset_kwargs)
    # instantiate model (only logistic regression for now)
    model = LogisticTwinModel()
    trainer = Trainer(model=model, dataset=data, threshold=args.threshold)
    result = trainer.run()
    # print results
    print("Factual accuracy:      {:.4f}".format(result.factual_accuracy))
    print("Counterfactual accuracy:{:.4f}".format(result.counterfactual_accuracy))
    print("Probability of necessity       (PN):  {:.4f}".format(result.prob_causation.pn))
    print("Probability of sufficiency     (PS):  {:.4f}".format(result.prob_causation.ps))
    print("Probability of necessity& suff (PNS):{:.4f}".format(result.prob_causation.pns))
    # print metadata as JSON
    print("\nMetadata:")
    print(json.dumps(result.metadata, indent=2, default=str))


if __name__ == '__main__':
    main(parse_args())