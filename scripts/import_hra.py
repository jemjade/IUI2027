"""Import a downloaded HRA ASCT+B table. No network calls or auto-assumed releases."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from scaleverify.hra import parse_asctb_csv  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize an official ASCT+B CSV into anatomical context")
    parser.add_argument("--input", required=True, help="Path to manually downloaded HRA ASCT+B CSV")
    parser.add_argument("--release", required=True, help="Release identifier verified on the HRA portal, e.g. v2.5")
    parser.add_argument("--organ", default="heart")
    parser.add_argument("--output", default=str(ROOT / "data" / "derived" / "heart_context.json"))
    args = parser.parse_args()
    graph = parse_asctb_csv(args.input, args.release, args.organ)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Imported {graph['metadata']['data_rows_parsed']} rows, {len(graph['nodes'])} nodes, {len(graph['edges'])} reference links")
    print("NOT evidence of disease causation:", output)


if __name__ == "__main__":
    main()
