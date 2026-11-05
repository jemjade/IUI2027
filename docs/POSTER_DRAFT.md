# IUI 2027 Poster — Working Manuscript v0.1

**Title:** ScaleVerify: An Inspectable Interface for Scale-Aware Evidence Triage in AI-Assisted Biomedical Discovery

**Status:** Work-in-progress draft as of 2026-11-05. **NOT yet a submission-ready paper.** No independent real-data evaluation or user study has been performed. Replace every bracketed item with **actual evidence only**.

## Abstract
AI-assisted biomedical discovery can produce hypotheses that connect molecular changes, cell types, tissues and organ-level outcomes. Researchers must determine which links warrant verification, but their attention and evidence-review effort are limited. We introduce ScaleVerify, an early-stage visual analytics prototype that represents candidate verification actions as cross-scale tasks and exposes a transparent, cost-constrained ranking. The interface provides a scale overview, a sortable verification queue, an inspection view of ranking factors, and separately labelled Human Reference Atlas anatomical reference context. A reproducible synthetic-data sanity check exercises budgeted ranking against simple baselines and a scale-feature ablation. These checks validate software behavior but do not establish improved scientific or human performance. We outline a source-backed study protocol for assessing whether scale-aware triage can help identify consequential evidence gaps at matched review effort. The research aims to advance inspectable, human-centered verification workflows rather than automate clinical or causal conclusions.

## 1. Motivation
AI tools may generate plausible biomedical hypotheses even when intermediate connections are weakly evidenced. Reviewing every connection is expensive; presenting a complex pathway is not equivalent to deciding which claims deserve attention first. A concrete task might involve a proposed molecule-to-cell relationship followed by a cell-to-organ relationship. Human experts need to separate anatomical reference structure, association, causal inference and conflicting or absent evidence.

We ask: **Can a scale-aware, cost-conscious verification queue help researchers identify consequential evidence gaps within a fixed inspection budget?**

Existing systems already support hypothesis construction and validation selection: HypoChainer uses LLMs, knowledge graphs and expert-guided exploration [1]. Multiscale biomedical graph navigation and evidence drill-down also have prior art [2]. Thus the potential novelty is *not* another generic biomedical knowledge graph, biological zoom interface or LLM hypothesis generator. The candidate contribution is a **verification-task triage workflow** that makes biological scale, inspection effort and evidence status visible and testable.

## 2. Prototype and Design Rationale
ScaleVerify models each candidate verification task using `from_scale`, `to_scale`, `uncertainty`, `consequence`, `missing_evidence`, `estimated_cost` and `evidence_status`. Missing and contradicting evidence are treated distinctly. The present heuristic score is

```
score = (0.32*consequence + 0.28*uncertainty
       + 0.24*scale_span + 0.16*missing_evidence)
       / (0.5 + estimated_cost)
```

The current weights are design placeholders, not a learned or validated model. A simple greedy budget selector proposes a shortlist, while the interface allows switching between ScaleVerify, Uncertainty-only, Evidence-gap-only and a seeded Random baseline. The right-hand detail view exposes inputs and warns that the numerical score is neither confidence nor causal evidence.

For anatomical context, a separate importer converts downloaded HRA ASCT+B CSV rows to a provenance-labelled reference graph. Hierarchical anatomical structures, cell type locations and biomarker characterizations remain distinct from hypothetical disease mechanisms. In the current delivered repository, actual HRA data **has not yet been downloaded or imported**, and the interface honestly displays that state. A small adjacency visualization is available after an import.

## 3. Preliminary Engineering Checks and Planned Evaluation
The source repository contains synthetic tasks, unit tests and read-only API behavior checks. The local tests cover reference graph parsing, duplicate-edge removal, stable ranking, budget enforcement and hiding evaluation-only labels from UI responses. **These tests establish software functionality only.** In the synthetic check with 10 hand-labelled examples, ScaleVerify ties other baselines at budget 6, and removing the scale feature does not change labelled-gap counts at budgets 3, 6 or 9. We therefore **do not claim any observed incremental benefit from scale awareness**.

A future evaluation will select one precisely scoped heart-related hypothesis family, obtain source-backed evidence links and report provenance, ontology mappings, biological context and what is merely associated rather than causal. Independent raters, blind to model ranking, will adjudicate consequential gaps. At fixed measured review budgets, we propose to compare gap recall, precision@k and actual review time against credible baselines, with scale-feature ablation and sensitivity analysis. Any interactive benefits, such as reduced cognitive load or improved trust calibration, require later human evaluation.

## 4. Limitations and Discussion
Biological scales are not simply distance levels: a larger scale span does not imply a less reliable link. Evidence absence is a statement about search scope, not falsity. Reference atlas mappings in healthy tissue do not verify causal drug or disease hypotheses. Cost estimates may be badly calibrated, and fixed heuristics can be brittle across tasks. Annotations and true observed inspection effort are still unavailable. The current UI is an early design artifact rather than an evaluated intelligent interface.

The immediate next step is to establish source-backed tasks and test whether biological-scale context meaningfully changes verification decisions, while keeping the human researcher responsible for evidence interpretation.

## Figure placeholders
- **Fig. 1:** Synthetic-scale task chain with verification queue and evidence status [use actual screenshot after visual QA].
- **Fig. 2:** Anatomical-reference context derived from **verifiably imported** HRA data [do not imply download is complete].
- **Fig. 3:** Real-data or separately labelled toy-only comparison with scale-feature ablation; ensure figure caption distinguishes these.

## References to check for correct ACM formatting
[1] Jiang et al. (2025). *HypoChainer: A Collaborative System Combining LLMs and Knowledge Graphs for Hypothesis-Driven Scientific Discovery*. IEEE TVCG. DOI: https://doi.org/10.1109/TVCG.2025.3633887

[2] Husain et al. (2021). *A Multi-Scale Visual Analytics Approach for Exploring Biomedical Knowledge*. VAHC. DOI: https://doi.org/10.1109/VAHC53616.2021.00010

[3] von Wyl and Bernard (2025). *Grand Challenge: Mediating Between Confirmatory and Exploratory Research Cultures in Health Sciences and Visual Analytics*. https://doi.org/10.48550/arXiv.2508.11544

**Submission checks:** IUI 2027 official Poster CFP; four pages excluding references; single-column ACM manuscript format; include CCS concepts; in-person attendance requirement; generative AI policy compliance. As a work-in-progress poster, avoid overstating completed research. Official CFP: https://iui.acm.org/2027/call-for-posters-demos/
