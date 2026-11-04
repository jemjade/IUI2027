"""Experimental, inspectable ranking and evaluation on synthetic tasks only."""
from __future__ import annotations
import json
import math
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

SCALES = ("molecule", "cell", "tissue", "organ", "organism")
STATUSES = ("support", "contradict", "mixed", "missing", "unreviewed")
METHODS = ("random", "uncertainty", "evidence_gap", "scaleverify")


@dataclass(frozen=True)
class Task:
    id: str
    label: str
    from_scale: str
    to_scale: str
    uncertainty: float
    consequence: float
    missing_evidence: bool
    estimated_cost: float
    evidence_status: str
    critical_gap_label: bool

    @classmethod
    def from_dict(cls, obj: dict) -> "Task":
        if not isinstance(obj["missing_evidence"], bool) or not isinstance(obj["critical_gap_label"], bool):
            raise ValueError("Boolean fields must be true or false")
        t = cls(**obj)
        if not t.id.strip() or not t.label.strip():
            raise ValueError("Task ID and label are required")
        if t.from_scale not in SCALES or t.to_scale not in SCALES:
            raise ValueError("Unknown biological scale")
        if t.evidence_status not in STATUSES:
            raise ValueError("Unknown evidence status")
        for field in ("uncertainty", "consequence"):
            value = getattr(t, field)
            if not isinstance(value, (int, float)) or not math.isfinite(value) or not 0 <= value <= 1:
                raise ValueError(field + " must be finite and in [0, 1]")
        if not isinstance(t.estimated_cost, (int, float)) or not math.isfinite(t.estimated_cost) or t.estimated_cost <= 0:
            raise ValueError("Cost must be finite and positive")
        if t.evidence_status == "missing" and not t.missing_evidence:
            raise ValueError("Inconsistent missing evidence status")
        return t

    @property
    def scale_span(self) -> float:
        return abs(SCALES.index(self.from_scale) - SCALES.index(self.to_scale)) / 4


def load_tasks(path: str | Path) -> list[Task]:
    rows = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(rows, list) or not rows:
        raise ValueError("Expected a nonempty list of tasks")
    tasks = [Task.from_dict(row) for row in rows]
    if len(set(t.id for t in tasks)) != len(tasks):
        raise ValueError("Duplicate task identifiers")
    return tasks


def experimental_score(task: Task) -> float:
    # Illustrative weights, not empirically fitted or clinically validated.
    # The evaluation-only critical_gap_label is intentionally never read.
    return (0.32 * task.consequence + 0.28 * task.uncertainty
            + 0.24 * task.scale_span + 0.16 * int(task.missing_evidence)
            ) / (0.5 + task.estimated_cost)


def rank_tasks(tasks: Iterable[Task], method: str, seed: int = 7) -> list[Task]:
    items = list(tasks)
    if method not in METHODS:
        raise ValueError(f"Unknown method: {method}")
    if method == "random":
        out = sorted(items, key=lambda x: x.id)
        random.Random(seed).shuffle(out)
        return out
    if method == "uncertainty":
        return sorted(items, key=lambda x: (-x.uncertainty, x.id))
    if method == "evidence_gap":
        return sorted(items, key=lambda x: (-int(x.missing_evidence), -x.consequence, x.id))
    return sorted(items, key=lambda x: (-experimental_score(x), x.id))


def select_with_budget(ranked: Iterable[Task], budget: float) -> list[Task]:
    if not math.isfinite(budget) or budget < 0:
        raise ValueError("Budget must be finite and nonnegative")
    selected: list[Task] = []
    used = 0.0
    for item in ranked:
        if used + item.estimated_cost <= budget + 1e-9:
            selected.append(item)
            used += item.estimated_cost
    return selected


def summarize(ranked: list[Task], selected: list[Task], top_k: int) -> dict:
    if top_k < 1:
        raise ValueError("top_k must be positive")
    positives = sum(x.critical_gap_label for x in ranked)
    found = sum(x.critical_gap_label for x in selected)
    top = ranked[:top_k]
    return dict(
        selected_task_ids=[x.id for x in selected],
        spent_cost_units=round(sum(x.estimated_cost for x in selected), 6),
        critical_gaps_found=found,
        total_critical_gaps=positives,
        recall_at_budget=round(found / positives, 4) if positives else None,
        precision_at_k=round(sum(x.critical_gap_label for x in top) / len(top), 4) if top else None,
    )


def compare(tasks: list[Task], budget: float = 6, top_k: int = 3, seed: int = 7) -> dict:
    if not tasks or not math.isfinite(budget) or budget < 0 or top_k < 1:
        raise ValueError("Invalid comparison arguments")
    result = dict(dataset="synthetic (illustrative only)", budget=budget, top_k=top_k, seed=seed, methods={})
    for method in METHODS:
        ranked = rank_tasks(tasks, method, seed)
        result["methods"][method] = summarize(ranked, select_with_budget(ranked, budget), top_k)
    return result
