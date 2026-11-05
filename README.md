# ScaleVerify

**Scale-Aware Evidence Triage for AI-Generated Biomedical Hypotheses**

Early-stage research prototype for ACM IUI 2027 Poster and a future CNS Talk. The research question: **Which cross-scale evidence link should be inspected first under limited verification effort?**

> **2026-11-05 status — v0.2:** Local interactive web prototype, synthetic verification-task ranking, budget sweep and an HRA ASCT+B CSV importer. The **actual HRA heart CSV is NOT bundled or imported**. No real biomedical accuracy or cognitive-load improvement has been established. This is **not** a diagnostic or clinical decision-support tool.

## Quick start (Python 3.10+, no external dependencies)

```bash
git clone https://github.com/jemjade/IUI2027.git
cd IUI2027
python3 -m unittest discover -s tests -v
python3 scripts/serve_demo.py
```

Then open **http://127.0.0.1:8765** in your browser.

In the demo, choose ScaleVerify, Uncertainty-only, Evidence-gap-only or Random and drag the review budget slider. The browser shows **synthetic** tasks, priority order, selected costs and transparent input features. The evaluation label is never returned by the UI API.

## Reproduce the synthetic evaluation

```bash
python3 scripts/run_demo.py --budget 6 --top-k 3
python3 scripts/benchmark_synthetic.py --budgets 3 6 9 --random-seeds 30
```

The synthetic benchmark also compares a **no-scale ablation**. The 0.32/0.28/0.24/0.16 weights and synthetic ground-truth labels are hand-designed, not scientifically validated. Synthetic differences are NOT scientific results.

## Load real HRA anatomical reference data (manual download)

1. Go to the official [HRA ASCT+B portal](https://humanatlas.io/asctb-tables).
2. Download the **heart CSV** and record the release shown on the portal. The 2026-11-05 portal showed the HRA v2.5 release and heart table version v1.7.
3. Import the CSV (replace the source path and release with the downloaded version):

```bash
python3 scripts/import_hra.py --input ~/Downloads/heart.csv --release v2.5 --organ heart
python3 scripts/serve_demo.py
```

The generated `data/derived/heart_context.json` preserves a source SHA-256, table row provenance, ontology identifiers when supplied, and reference-only relationship types. It is ignored by git until the source license and attribution have been checked. The importer was verified with a **constructed example CSV only** and might need adjustment to match a future source schema.

The HRA section of the interface will remain visibly unavailable until a real CSV is imported. Its structures and biomarkers are **anatomical reference context**, not evidence that any gene causes disease or that a drug works.

## Project structure

- [Research plan](docs/RESEARCH_PLAN.md)
- [Build log and limitations](docs/PROGRESS_2026-11-05.md)
- [Annotation rubric](docs/ANNOTATION_RUBRIC.md)
- [Data and annotation protocol](docs/DATA_PROTOCOL.md)
- [Prior literature](docs/LITERATURE.md)
- [IUI Poster outline](docs/POSTER_OUTLINE.md)
- `src/scaleverify/core.py`: heuristic ranking and budget selection
- `src/scaleverify/benchmark.py`: budget sweep, random-seed checks and scale ablation
- `src/scaleverify/hra.py`: ASCT+B CSV to provenance-labelled anatomical reference graph
- `scripts/serve_demo.py`, `web/index.html`: local read-only API and visual interface
- `tests/`: unit tests for ranking, importer, budget comparison and web API

## Scientific boundaries

- Do not mistake *missing evidence* for *evidence against* a claim.
- Do not treat HRA's healthy anatomical data as proof of a disease mechanism.
- Pre-register a source-backed, independently annotated task set before claiming effectiveness.
- Do not assert reduced cognitive load without a human evaluation.
- See [HypoChainer (Jiang et al., IEEE TVCG 2025)](https://doi.org/10.1109/TVCG.2025.3633887): hypothesis-guided validation selection is already prior work. Our candidate novelty is **scale-aware and cost-conscious verification task triage**, pending validation.

This software is a research prototype only.