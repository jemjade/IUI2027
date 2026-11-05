"""Serve the research-only interface and two read-only JSON APIs; stdlib only.

The only public files are web/index.html and the computed read-only API data.
Evaluation-only ground-truth labels are never returned as task-level fields.
"""
from __future__ import annotations

import argparse
import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from scaleverify.core import METHODS, experimental_score, load_tasks, rank_tasks, select_with_budget, summarize


class Handler(BaseHTTPRequestHandler):
    def _reply(self, code: int, body: bytes, content_type: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, code: int, data: dict) -> None:
        self._reply(code, json.dumps(data, ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8")

    def do_GET(self) -> None:
        parsed = urlsplit(self.path)
        if parsed.path in ("/", "/index.html"):
            self._reply(200, (ROOT / "web" / "index.html").read_bytes(), "text/html; charset=utf-8")
            return
        if parsed.path == "/api/context":
            path = ROOT / "data" / "derived" / "heart_context.json"
            if path.exists():
                self._json(200, {"available": True, "context": json.loads(path.read_text(encoding="utf-8"))})
            else:
                self._json(200, {"available": False, "message": "No HRA file imported. Download official CSV and run scripts/import_hra.py."})
            return
        if parsed.path == "/api/rank":
            try:
                params = parse_qs(parsed.query)
                method = params.get("method", ["scaleverify"])[0]
                budget = float(params.get("budget", ["6"])[0])
                seed = int(params.get("seed", ["7"])[0])
                if method not in METHODS or not 0 <= budget <= 1000 or abs(seed) > 1000000:
                    raise ValueError("Invalid method, budget or seed")
                tasks = load_tasks(ROOT / "data" / "synthetic" / "verification_tasks.json")
                ranked = rank_tasks(tasks, method, seed)
                selected = select_with_budget(ranked, budget)
                selected_ids = {t.id for t in selected}
                records = [{
                    "id": t.id, "label": t.label, "from_scale": t.from_scale, "to_scale": t.to_scale,
                    "uncertainty": t.uncertainty, "consequence": t.consequence,
                    "scale_span": t.scale_span, "missing_evidence": t.missing_evidence,
                    "estimated_cost": t.estimated_cost, "evidence_status": t.evidence_status,
                    "heuristic_score": round(experimental_score(t), 4),
                    "selected_under_budget": t.id in selected_ids,
                } for t in ranked]
                # Evaluation-only labels are deliberately excluded from records.
                summary = summarize(ranked, selected, top_k=min(3, len(tasks)))
                self._json(200, {"dataset": "SYNTHETIC ONLY", "method": method, "budget": budget,
                                 "tasks": records, "selected_count": len(selected), "spent_cost_units": summary["spent_cost_units"],
                                 "note": "A demonstration, not biomedical evidence, human evaluation or verified clinical reasoning."})
            except (ValueError, KeyError, TypeError) as exc:
                self._json(400, {"error": str(exc)})
            return
        self._json(404, {"error": "Not found"})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=8765, type=int)
    args = parser.parse_args()
    with ThreadingHTTPServer((args.host, args.port), Handler) as server:
        print(f"ScaleVerify prototype: http://{args.host}:{args.port}")
        print("Synthetic tasks are never represented as real biomedical evidence.")
        server.serve_forever()


if __name__ == "__main__":
    main()
