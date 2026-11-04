# Data and annotation protocol

## Task schema
- `id`: stable, unique task key.
- `label`: descriptive non-clinical task name.
- `from_scale` / `to_scale`: molecule, cell, tissue, organ or organism.
- `uncertainty`, `consequence`: defined scores in [0, 1]. **Not probabilities of falsity.**
- `missing_evidence`: whether the *documented search protocol* found no admissible evidence.
- `estimated_cost`: positive review-effort units, **not measured minutes or dollars**.
- `evidence_status`: support, contradict, mixed, missing or unreviewed.
- `critical_gap_label`: evaluation-only label; must never be an input to ranking.

## Real dataset extension
Record DOI/URL, date retrieved, source version/license, organism, tissue, ontology IDs (UBERON, CL, UniProt/HGNC as applicable), assay type, statistics, statement direction, evidence quality, causality-versus-association classification, annotator ID and agreement, and raw verification-time measurement if available.

## Source separation
- [Human Reference Atlas](https://humanatlas.io/): anatomical structures, cell types and biomarkers as reference context.
- [Reactome](https://reactome.org/): pathway context with provenance.
- [Open Targets](https://platform.opentargets.org/): target-disease association evidence, not automatic causal proof.
- [PubMed](https://pubmed.ncbi.nlm.nih.gov/): link to original publications and inspect study methods.

## Protocol
1. Pre-register source selection and intended evaluation.
2. Blind annotators to model ranking and method outputs.
3. Split cases before tuning. Keep labels separate from model features for real data.
4. Missing evidence != evidence against. Contradictory evidence != absence.
5. Record exact data versions and source permissions.
6. Never use synthetic labels as a biomedical benchmark.
7. Do not infer cross-scale causal validity from anatomical or ontology mappings.
