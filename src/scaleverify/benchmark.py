"""Synthetic-only budget curves and scale-feature ablation.

Labels are used ONLY when computing metrics, never by ranking functions.
This is a software sanity check, not a biomedical experiment.
"""
from __future__ import annotations
import math
from statistics import mean
from .core import Task, experimental_score, rank_tasks, select_with_budget


def _rank_without_scale(tasks: list[Task]) -> list[Task]:
    return sorted(tasks, key=lambda t: (-(experimental_score(t) - 0.24 * t.scale_span / (0.5 + t.estimated_cost)), t.id))


def _measure(items: list[Task], budget: float) -> dict:
    selected = select_with_budget(items, budget)
    all_critical = sum(t.critical_gap_label for t in items)
    found = sum(t.critical_gap_label for t in selected)
    spent = sum(t.estimated_cost for t in selected)
    return {"critical_gaps_found": found, "recall_at_budget": found / all_critical if all_critical else None,
            "spent_cost_units": round(spent, 5), "critical_gaps_per_cost_unit": found / spent if spent else None}


def budget_sweep(tasks: list[Task], budgets: list[float], random_seeds: int = 30) -> dict:
    if not tasks or any((not math.isfinite(b) or b <= 0) for b in budgets) or not budgets:
        raise ValueError("Tasks and positive budgets are required")
    if not 1 <= random_seeds <= 10000:
        raise ValueError("random_seeds must be between 1 and 10000")
    curves = []
    for budget in budgets:
        runs = {m: _measure(rank_tasks(tasks, m), budget) for m in ("scaleverify", "uncertainty", "evidence_gap")}
        runs["no_scale_ablation"] = _measure(_rank_without_scale(tasks), budget)
        random_runs = [_measure(rank_tasks(tasks, "random", seed), budget) for seed in range(random_seeds)]
        runs["random"] = {"critical_gaps_found_mean": mean(x["critical_gaps_found"] for x in random_runs),
                          "critical_gaps_found_min": min(x["critical_gaps_found"] for x in random_runs),
                          "critical_gaps_found_max": max(x["critical_gaps_found"] for x in random_runs),
                          "seeds": random_seeds}
        curves.append({"budget": budget, "methods": runs})
    return {"dataset": "synthetic, hand-labelled (not biomedical evidence)",
            "warning": "Illustrative sanity check only. No data-independent or human performance claims.",
            "curves": curves}
