# ScaleVerify Synthetic-Only Sanity Check (2026-11-05)

**Not a scientific evaluation.** The ten tasks, estimated costs, feature scores and five positive `critical_gap_label` values were manually invented to test code behavior. The evaluation labels are not independently annotated or source-backed. All numbers below are illustrative and must not be cited as biomedical performance.

## How to reproduce
```bash
python3 scripts/benchmark_synthetic.py --budgets 3 6 9 --random-seeds 30
```

## Number of hand-labelled critical gaps selected under each budget

| Ranking method | Budget 3 | Budget 6 | Budget 9 |
| --- | ---: | ---: | ---: |
| ScaleVerify heuristic | 2 | 3 | 5 |
| Uncertainty-only | 1 | 3 | 5 |
| Evidence-gap-only | 2 | 3 | 5 |
| ScaleVerify without scale feature | 2 | 3 | 5 |
| Random, mean over seeds 0–29 | 0.83 | 2.10 | 3.13 |

Five invented tasks were designated positive, so illustrative Recall@Budget for ScaleVerify is 0.40, 0.60 and 1.00 respectively. Counts for random are arithmetic means over seeds, not observed biological discoveries or statistically independent trials.

## Interpretation
- The prototype demonstrates that ranking, cost constraints, label hiding and comparison tooling function as intended.
- At budget 6 **ScaleVerify, Uncertainty-only, Evidence-gap-only and no-scale ablation tie**.
- The no-scale ablation selects the same number of labelled gaps at all evaluated budgets, so this synthetic example provides **no evidence that biological scale improves ranking**.
- The synthetic labels may be correlated with the manually designed features, making any apparent advantage circular.

## What must happen next
Collect real, source-backed cross-scale verification tasks, obtain independent blind critical-gap labels, measure actual inspection effort, and evaluate held-out cases including a meaningful scale-agnostic baseline. Report failures and uncertainty; do not retrofit the formula to this toy benchmark then claim generalization.
