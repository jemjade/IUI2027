"""Print transparent synthetic benchmark results; not for scientific performance claims."""
import argparse
import json
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from scaleverify.benchmark import budget_sweep  # noqa: E402
from scaleverify.core import load_tasks  # noqa: E402


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--budgets", nargs="+", type=float, default=[3, 6, 9])
    parser.add_argument("--random-seeds", type=int, default=30)
    args = parser.parse_args()
    tasks = load_tasks(ROOT / "data" / "synthetic" / "verification_tasks.json")
    result = budget_sweep(tasks, args.budgets, args.random_seeds)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
