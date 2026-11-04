# IUI 2027 Poster outline (draft)

**Proposed title:** ScaleVerify: Scale-Aware Evidence Triage for AI-Generated Biomedical Hypotheses

## Candidate abstract
AI-assisted biomedical discovery increasingly involves hypotheses spanning molecular, cellular, tissue and organ scales. Such links require evidence inspection, yet researcher attention and verification effort are limited. We propose ScaleVerify, an inspectable framework that represents cross-scale claims as evidence-verification tasks and ranks them by uncertainty, consequence, biological span, evidence gap and estimated inspection cost. The proposed visual workflow combines a scale-aware graph, a verification queue and a provenance panel. We describe the design and evaluation protocol, compare against transparent baselines, and discuss the distinction between anatomical references and causal validation. [INSERT ONLY ACTUALLY COMPLETED DATASET AND EMPIRICAL RESULTS.]

## Provisional four-page structure
1. Introduction, concrete verification task and relevant prior work
2. System and explainable ranking with visual interface
3. Source-backed data and *actually performed* evaluation
4. Discussion, limitations and future validation

## Figure plan
- Hypothesis edge diagram with support / contradiction / missing evidence distinguished
- Three coordinated views: graph + ranked queue + source provenance
- Equal-budget comparison **only when real annotated data exists**

## Submit checks
- [ ] Verify up-to-date official IUI CFP and ACM template
- [ ] Verify page limit, references, deadline and time zone
- [ ] Add data provenance, source licenses, assessment protocol
- [ ] Exclude toy results from biomedical performance conclusions
- [ ] Clearly label untested usability and clinical claims
