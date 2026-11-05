import csv
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from scaleverify.hra import parse_asctb_csv


class HRAImportTests(unittest.TestCase):
    def _make_csv(self, path):
        rows = [["metadata", "", "", "", "", "", "", "", "", "", ""] for _ in range(10)]
        rows.append(["AS/1", "AS/1/ID", "AS/2", "AS/2/ID", "CT/1", "CT/1/ID", "BG/1", "BG/1/ID"])
        rows.extend([
            ["heart", "UBERON:0000948", "cardiac muscle tissue", "UBERON:0001133", "cardiomyocyte", "CL:0000746", "ACTC1", "HGNC:143"],
            ["heart", "UBERON:0000948", "cardiac muscle tissue", "UBERON:0001133", "cardiomyocyte", "CL:0000746", "ACTC1", "HGNC:143"],
        ])
        with open(path, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerows(rows)

    def test_hra_header_and_relationships(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "heart.csv"
            self._make_csv(p)
            graph = parse_asctb_csv(p, release="test-only")
        self.assertEqual(graph["metadata"]["header_row"], 11)
        self.assertEqual(graph["metadata"]["data_rows_parsed"], 2)
        self.assertEqual(graph["metadata"]["node_count"], 4)
        self.assertEqual(graph["metadata"]["edge_count"], 3)
        self.assertEqual({x["relation"] for x in graph["edges"]}, {"part_of", "located_in", "characterized_by"})
        self.assertTrue(all(x["evidence_type"] == "anatomical_reference" for x in graph["edges"]))
        self.assertTrue(all(x["source_rows"] == [12, 13] for x in graph["edges"]))

    def test_invalid_columns(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "bad.csv"
            p.write_text("hello,world\na,b\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "header"):
                parse_asctb_csv(p, release="test-only")


if __name__ == "__main__":
    unittest.main()
