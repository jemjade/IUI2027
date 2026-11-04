import sys
import unittest
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from scaleverify.core import Task, compare, experimental_score, load_tasks, rank_tasks, select_with_budget


class CoreTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tasks = load_tasks(ROOT / "data" / "synthetic" / "verification_tasks.json")

    def test_load(self):
        self.assertEqual(len(self.tasks), 10)

    def test_label_leakage(self):
        item = self.tasks[0]
        self.assertEqual(experimental_score(item), experimental_score(replace(item, critical_gap_label=False)))

    def test_uncertainty_monotonicity(self):
        item = self.tasks[0]
        self.assertGreater(experimental_score(item), experimental_score(replace(item, uncertainty=0.1)))

    def test_scale_span(self):
        self.assertEqual(self.tasks[3].scale_span, 0.75)

    def test_random_order_independent_of_input(self):
        a = rank_tasks(self.tasks, "random", 7)
        b = rank_tasks(list(reversed(self.tasks)), "random", 7)
        self.assertEqual([x.id for x in a], [x.id for x in b])

    def test_budget(self):
        for method in ("random", "uncertainty", "evidence_gap", "scaleverify"):
            ranked = rank_tasks(self.tasks, method)
            selected = select_with_budget(ranked, 3)
            self.assertLessEqual(sum(x.estimated_cost for x in selected), 3.000000001)

    def test_missing_status_validation(self):
        altered = vars(self.tasks[0]).copy()
        altered["missing_evidence"] = False
        with self.assertRaises(ValueError):
            Task.from_dict(altered)

    def test_comparison(self):
        result = compare(self.tasks)
        self.assertEqual(len(result["methods"]), 4)
        for row in result["methods"].values():
            self.assertLessEqual(row["spent_cost_units"], 6)

    def test_invalid_budget(self):
        with self.assertRaises(ValueError):
            compare(self.tasks, budget=-1)


if __name__ == "__main__":
    unittest.main()
