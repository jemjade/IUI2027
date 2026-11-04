# ScaleVerify 연구계획서 v0.1

## 제목
ScaleVerify: Scale-Aware Evidence Triage for AI-Generated Biomedical Hypotheses

## 문제 정의
AI가 생의학 가설을 생성하더라도 분자, 세포, 조직, 장기 수준을 잇는 주장에는 서로 다른 자료의 검증되지 않은 연결이 존재한다. 제한된 검토 예산 안에서 **어떤 근거 연결을 먼저 검증할지** 선택하는 작업을 연구한다. HRA는 해부학적 참조 정보를 제공하며 질병의 인과관계를 직접 증명하지 않는다.

## Research Questions
- **RQ1:** Does scale-aware triage identify more *independently annotated consequential evidence gaps* than scale-agnostic baselines at matched review budgets?
- **RQ2:** Can an inspectable interface help researchers distinguish support, contradiction and absent evidence? RQ2 requires human evaluation and has not been tested.
- **RQ3 (future):** How should HRA anatomy anchor cross-scale hypotheses without implying causal biomedical validation?

## Method (prototype only)
A verification task represents an edge/link between claims with biological levels, uncertainty, consequence, missing-evidence status and estimated effort. The experimental heuristic is:

```
priority = (0.32 * consequence
          + 0.28 * uncertainty
          + 0.24 * biological_scale_span
          + 0.16 * missing_evidence) / (0.5 + estimated_cost)
```

The features are normalized and the weights are **illustrative, not learned or validated**. Ranking is followed by greedy selection under a common budget. Scale span is not itself evidence of unreliability.

## Evaluation plan
1. Run synthetic unit tests to check reproducibility and prevent label leakage (not a scientific outcome).
2. Select one narrow heart-related question and source-backed biological entities and claims.
3. Record HRA ASCT+B anatomical context separately from externally sourced biomedical evidence.
4. Obtain blind, independently assigned labels for consequential evidence gaps, and document annotator agreement.
5. Compare Random, Uncertainty-only, Evidence-gap-only and ScaleVerify at the same effort budget.
6. Report critical gaps found, recall at budget, precision@K and sensitivity to ranking weights. Distinguish estimated effort units from observed researcher time.
7. Future human evaluation of comprehension, trust calibration and cognitive load is required before claiming usability benefits.

## Novelty boundary
HypoChainer already includes visual hypothesis exploration and validation selection; scale-aware, cost-conscious **verification task ranking**, if supported by an appropriate benchmark, is the candidate contribution. Neither an LLM/KG pipeline nor biological zooming alone is novel.

## Deliverables and go/no-go
- Research plan and evidence schema
- Reproducible ranking, baseline, unit tests
- Prototype showing a scale graph, ranked verification tasks and provenance
- Source-backed, independent evaluation before any performance claim

**Go/no-go:** if a trustworthy source-backed task set and reference labels cannot be obtained, present it as preliminary system design, not as experimentally validated medical discovery.

## CNS Talk
Frame the progression: Verify-First → cross-scale verification → Evidence-Aware Biomedical Discovery. Clearly distinguish completed results, prototype and future work.