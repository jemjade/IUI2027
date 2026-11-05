import sys
import unittest
from dataclasses import replace
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from scaleverify.benchmark import _rank_without_scale, budget_sweep
from scaleverify.core import Task


class BenchmarkTests(unittest.TestCase):
    def setUp(self):
        self.tasks = [
            Task(id="A", label="A", from_scale="molecule", to_scale="organ", uncertainty=.9, consequence=.8, missing_evidence=True, estimated_cost=1, evidence_status="missing", critical_gap_label=True),
            Task(id="B", label="B", from_scale="cell", to_scale="cell", uncertainty=.4, consequence=.2, missing_evidence=False, estimated_cost=1, evidence_status="support", critical_gap_label=False),
        ]

    def test_same_scores_when_labels_flipped(self):
        before = _rank_without_scale(self.tasks)
        after = _rank_without_scale([replace(t, critical_gap_label=not t.critical_gap_label) for t in self.tasks])
        self.assertEqual([x.id for x in before], [x.id for x in after])

    def test_seed_sweep_and_budget(self):
        result = budget_sweep(self.tasks, [1, 2], 10)
        self.assertEqual(len(result["curves"]), 2)
        self.assertEqual(result["curves"][0]["methods"]["random"]["seeds"], 10)
        self.assertTrue(all(r["methods"]["scaleverify"]["spent_cost_units"] <= r["budget"] for r in result["curves"]))

    def test_invalid(self):
        with self.assertRaises(ValueError):
            budget_sweep(self.tasks, [-1])
