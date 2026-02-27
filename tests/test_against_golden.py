from __future__ import annotations

import json
import unittest
from pathlib import Path

from src.engine.run import run_valuation

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "spec" / "schema.json"
INPUT_PATH = ROOT / "data" / "samples" / "sample_inputs_1.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


class TestEngineSmoke(unittest.TestCase):
    def test_engine_smoke(self) -> None:
        payload = load_json(INPUT_PATH)
        result = run_valuation(payload, schema_path=SCHEMA_PATH)

        self.assertIn("projections", result)
        self.assertIn("valuation", result)

        projections = result["projections"]
        valuation = result["valuation"]

        years = payload["meta"]["years"]
        self.assertEqual(len(projections["revenue"]), years)
        self.assertEqual(len(projections["ebitda"]), years)
        self.assertEqual(len(projections["fcf"]), years)

        self.assertGreater(valuation["dcf"]["enterprise_value"], 0)
        self.assertIsInstance(valuation["football_field"]["low"], float)
        self.assertIsInstance(valuation["football_field"]["mid"], float)
        self.assertIsInstance(valuation["football_field"]["high"], float)


if __name__ == "__main__":
    unittest.main()
