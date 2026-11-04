# ScaleVerify

**Scale-Aware Evidence Triage for AI-Generated Biomedical Hypotheses**

An experimental research prototype for an **ACM IUI 2027 poster** and later **CNS talk**. It investigates *which cross-scale evidence link to inspect next* under a constrained verification budget.

> **Status (2026-11-03):** Reproducible **synthetic-data software scaffold**. No validated biomedical results, expert evaluations, or user-study findings. The weights and synthetic labels are illustrative, NOT scientifically validated.

## Research scope

- **Task:** rank which evidence links to verify, not diagnoses or treatments.
- **Scales:** molecule, cell, tissue, organ, organism.
- **Evidence:** distinguish supporting, contradictory, missing, mixed and unreviewed evidence.
- **Source roles:** HRA / ASCT+B supplies anatomical reference context, NOT proof of pathological causality.

## Run locally

Python 3.10+; no external dependencies.

```bash
python -m unittest discover -s tests -v
python scripts/run_demo.py --budget 6 --top-k 3
python scripts/run_demo.py --budget 6 --top-k 3 --json
```

The demo uses only `data/synthetic/verification_tasks.json`. Its results are **not evidence of improved biomedical research performance**.

## Directory map

- [Research plan](docs/RESEARCH_PLAN.md) (Korean)
- [Data and annotation protocol](docs/DATA_PROTOCOL.md)
- [Closest prior work](docs/LITERATURE.md)
- [Poster outline](docs/POSTER_OUTLINE.md)
- `src/scaleverify/core.py`: ranking and budgeted evaluation
- `scripts/run_demo.py`: reproducible synthetic comparison
- `tests/test_core.py`: deterministic behavior and leakage tests

## Primary research question

Can a scale-aware evidence-verification queue identify **more independently labeled consequential verification gaps at the same inspection budget** than uncertainty-only, evidence-gap-only and random baselines?

**Not clinical software.** Association and anatomical reference structure are not causality. Human-centered performance and biological relevance remain to be evaluated.
