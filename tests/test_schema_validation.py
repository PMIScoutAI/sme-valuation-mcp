from __future__ import annotations

import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "spec" / "schema.json"
VALID_SAMPLE = ROOT / "data" / "samples" / "sample_inputs_1.json"
INVALID_SAMPLE = ROOT / "data" / "samples" / "sample_inputs_invalid.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


class TestSchemaValidation(unittest.TestCase):
    def test_schema_valid_sample_passes(self) -> None:
        schema = load_json(SCHEMA_PATH)
        payload = load_json(VALID_SAMPLE)
        validator = Draft202012Validator(schema)
        errors = list(validator.iter_errors(payload))
        self.assertFalse(errors)

    def test_schema_invalid_sample_fails(self) -> None:
        schema = load_json(SCHEMA_PATH)
        payload = load_json(INVALID_SAMPLE)
        validator = Draft202012Validator(schema)
        errors = list(validator.iter_errors(payload))
        self.assertTrue(errors)


if __name__ == "__main__":
    unittest.main()
