"""Run a reproducible synthetic example. Not a biological benchmark."""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from scaleverify.core import compare, load_tasks  # noqa: E402


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--budget", type=float, default=6.0)
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    tasks = load_tasks(ROOT / "data" / "synthetic" / "verification_tasks.json")
    result = compare(tasks, args.budget, args.top_k, args.seed)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print("SYNTHETIC DEMO ONLY — no biomedical performance conclusions")
        print(f"Budget={args.budget:g} illustrative units; top-k={args.top_k}; seed={args.seed}")
        print("Method           Found   Recall@budget  Precision@k  Cost")
        for name, row in result["methods"].items():
            print(f"{name:16} {row['critical_gaps_found']:5}   {row['recall_at_budget']!s:>12}   "
                  f"{row['precision_at_k']!s:>11}  {row['spent_cost_units']:>5}")
            print("   Selected:", ", ".join(row["selected_task_ids"]))


if __name__ == "__main__":
    main()
