"""Convert an HRA ASCT+B CSV into a provenance-labelled anatomical reference graph.

No causal biomedical verification claims are inferred from an ASCT+B relationship.
"""
from __future__ import annotations

import csv
import hashlib
import re
from pathlib import Path

LEVELS = ("AS", "CT", "BG", "BP", "BM", "BF", "BL")
HEAD = re.compile(r"^(AS|CT|BG|BP|BM|BF|BL)/(\d+)(?:/(LABEL|ID))?$", re.I)
TYPE = {"AS": "anatomical_structure", "CT": "cell_type", "BG": "gene_biomarker", "BP": "protein_biomarker", "BM": "metabolite_biomarker", "BF": "proteoform_biomarker", "BL": "lipid_biomarker"}


def _find_header(rows: list[list[str]]) -> int:
    """HRA CSVs can include ~10 metadata rows ahead of the schema header."""
    for i, row in enumerate(rows):
        heads = {cell.strip().upper() for cell in row}
        if ("AS/1" in heads or "AS/1/LABEL" in heads) and any(cell.startswith("CT/") for cell in heads):
            return i
    raise ValueError("No ASCT+B header found; expected AS/1 and CT/1 columns")


def _entities(row: dict[str, str], prefix: str) -> list[dict]:
    level_nums = set()
    for col in row:
        match = HEAD.match(col)
        if match and match.group(1).upper() == prefix:
            level_nums.add(int(match.group(2)))
    found = []
    for n in sorted(level_nums):
        base = f"{prefix}/{n}"
        # The author-preferred term and ontology-preferred label may differ.
        label = (row.get(base) or row.get(base + "/LABEL") or "").strip()
        ontology_id = (row.get(base + "/ID") or "").strip()
        if label:
            found.append({"label": label, "ontology_id": ontology_id, "kind": TYPE[prefix], "level": n})
    return found


def parse_asctb_csv(path: str | Path, release: str, organ: str = "heart") -> dict:
    path = Path(path)
    raw = path.read_bytes()
    if not raw:
        raise ValueError("Empty CSV")
    text = raw.decode("utf-8-sig")
    rows = list(csv.reader(text.splitlines()))
    header_i = _find_header(rows)
    fields = [key.strip().upper() for key in rows[header_i]]
    if len(fields) != len(set(fields)):
        raise ValueError("Duplicate column headers")
    nodes: dict[str, dict] = {}
    edges: dict[tuple[str, str, str], dict] = {}
    parsed_rows = 0

    def add_entity(e: dict) -> str:
        # No ontology ID => fall back to a deterministic label-scoped key.
        slug = e["ontology_id"] or e["label"].casefold()
        key = f"{e['kind']}:{slug}"
        if key not in nodes:
            nodes[key] = {"id": key, "label": e["label"], "ontology_id": e["ontology_id"], "kind": e["kind"], "source": "HRA ASCT+B anatomical reference"}
        return key

    def add_edge(source: str, target: str, relation: str, row_number: int) -> None:
        key = (source, target, relation)
        if key not in edges:
            edges[key] = {"source": source, "target": target, "relation": relation, "source_rows": [], "evidence_type": "anatomical_reference"}
        if row_number not in edges[key]["source_rows"]:
            edges[key]["source_rows"].append(row_number)

    for row_number, values in enumerate(rows[header_i + 1:], start=header_i + 2):
        if not any(value.strip() for value in values):
            continue
        cells = dict(zip(fields, values))
        anatomy = _entities(cells, "AS")
        types = _entities(cells, "CT")
        biomarkers = [entry for prefix in LEVELS[2:] for entry in _entities(cells, prefix)]
        if not (anatomy or types or biomarkers):
            continue
        parsed_rows += 1
        anatomical_ids = [add_entity(e) for e in anatomy]
        cell_ids = [add_entity(e) for e in types]
        marker_ids = [add_entity(e) for e in biomarkers]
        for parent, child in zip(anatomical_ids, anatomical_ids[1:]):
            add_edge(child, parent, "part_of", row_number)
        if anatomical_ids:
            for cell_id in cell_ids:
                add_edge(cell_id, anatomical_ids[-1], "located_in", row_number)
        for cell_id in cell_ids:
            for marker_id in marker_ids:
                add_edge(cell_id, marker_id, "characterized_by", row_number)

    if parsed_rows == 0 or not nodes:
        raise ValueError("No anatomical relationships parsed; review CSV headers")
    return {
        "metadata": {
            "organ": organ,
            "release": release,
            "source_file": path.name,
            "source_sha256": hashlib.sha256(raw).hexdigest(),
            "source_page": "https://humanatlas.io/asctb-tables",
            "dataset_kind": "anatomical_reference",
            "warning": "Anatomical, cellular and biomarker relationships are NOT evidence of disease causation or treatment effects.",
            "data_rows_parsed": parsed_rows,
            "header_row": header_i + 1,
            "node_count": len(nodes),
            "edge_count": len(edges),
        },
        "nodes": sorted(nodes.values(), key=lambda x: x["id"]),
        "edges": sorted(edges.values(), key=lambda x: (x["source"], x["target"], x["relation"])),
    }
