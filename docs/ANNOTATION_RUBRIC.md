# ScaleVerify source-backed annotation rubric (draft)

## Unit of analysis
Each item is a **specific proposed evidence-verification task**, not an entire disease mechanism. Include: subject, relation, object, organism/context, source DOI/URL, supporting/contradicting documents, ontology IDs and whether a cross-scale mapping is anatomical, statistical or causal.

## Label instructions
- **Support**: relevant source explicitly supports the *specified* proposition under applicable conditions.
- **Contradict**: relevant source explicitly reports an incompatible result under comparable conditions.
- **Mixed**: credible applicable studies disagree; record reasons for disagreement.
- **Missing**: the preregistered search finds no eligible evidence; does NOT mean false.
- **Unreviewed**: not yet evaluated. Never call this missing.

## Proposed reviewer form
1. Claim ID and precise evidence link
2. Mechanism / association / anatomical-reference classification
3. Organism; subject population; disease / health status; assay and scale
4. Ontology mapping IDs and timestamps
5. Source IDs (DOI, PMID, HRA version), exact supports or contradicts claims
6. Evidence status and supporting excerpt location
7. Importance / consequence (0 to 1) with explicit project-specific anchors
8. Uncertainty (0 to 1) with explanation; **not interpreted as a calibrated probability**
9. Estimated inspection effort (before reading) and observed review effort (after reading)
10. Independent binary critical-gap label and confidence, hidden during model ranking

## Critical-gap reference label (to finalize with domain experts)
An item qualifies only if (a) its verification could materially alter the selected hypothesis chain or next action and (b) current evidence is inadequate/contested under documented criteria. Score independently and blind to ScaleVerify rank. Record disagreements and adjudication; compute inter-rater agreement when feasible. Avoid using the ranking features themselves as the ground-truth rubric to prevent circular evaluation.

## Required safeguards
- Anatomical located_in and biomarker characterized_by **do not** prove molecular-to-disease causality.
- Separate healthy HRA context from disorder, drug intervention and patient-outcome data.
- Relevance and provenance must be checked before calling an evidence item supportive or contradictory.
- No study participant, expert annotation or experimental result is claimed until actually collected.
- Do not cite manually invented or synthetic claims as real mechanistic results.
