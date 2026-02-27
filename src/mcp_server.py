from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from src.engine.run import run_valuation as engine_run_valuation

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "spec" / "schema.json"
MODEL_SPEC_PATH = ROOT / "spec" / "model_spec.yaml"
SAMPLES_PATH = ROOT / "data" / "samples"


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _validate_payload(payload: dict[str, Any]) -> list[str]:
    schema = _load_json(SCHEMA_PATH)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda e: e.path)
    return [e.message for e in errors]


try:
    from mcp.server.fastmcp import FastMCP  # type: ignore
except Exception:  # pragma: no cover
    FastMCP = None


if FastMCP is not None:
    mcp = FastMCP("sme-valuation-engine")

    @mcp.tool()
    def validate_input(payload_json: str) -> dict[str, Any]:
        payload = json.loads(payload_json)
        errors = _validate_payload(payload)
        return {
            "ok": len(errors) == 0,
            "errors": errors,
        }

    @mcp.tool()
    def run_valuation(payload_json: str) -> dict[str, Any]:
        payload = json.loads(payload_json)
        return engine_run_valuation(payload, schema_path=SCHEMA_PATH)

    @mcp.tool()
    def get_model_spec() -> str:
        return MODEL_SPEC_PATH.read_text(encoding="utf-8-sig")

    @mcp.tool()
    def list_scenarios() -> list[str]:
        if not SAMPLES_PATH.exists():
            return []
        return sorted(p.name for p in SAMPLES_PATH.glob("*.json"))


def main() -> None:
    if FastMCP is None:
        raise RuntimeError(
            "mcp package not installed. Install with: pip install mcp"
        )
    mcp.run()


if __name__ == "__main__":
    main()
