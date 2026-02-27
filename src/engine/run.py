from __future__ import annotations

import argparse
import json
from pathlib import Path

from jsonschema import Draft202012Validator

from .dcf import compute_dcf
from .football_field import compute_football_field
from .multiples import compute_multiples
from .projections import project_financials


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _validate_input(payload: dict, schema_path: Path | None) -> None:
    if schema_path is None:
        return
    schema = _load_json(schema_path)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda e: e.path)
    if errors:
        messages = "; ".join(err.message for err in errors)
        raise ValueError(f"Input validation failed: {messages}")


def run_valuation(payload: dict, schema_path: Path | None = None) -> dict:
    _validate_input(payload, schema_path=schema_path)

    projections = project_financials(payload)
    dcf = compute_dcf(payload, projections.fcf)
    mult = compute_multiples(payload, projections.ebitda)
    ff = compute_football_field(dcf.equity_value, mult.equity_value)

    return {
        "projections": {
            "revenue": projections.revenue,
            "ebitda": projections.ebitda,
            "fcf": projections.fcf,
        },
        "valuation": {
            "dcf": {
                "enterprise_value": dcf.enterprise_value,
                "equity_value": dcf.equity_value,
            },
            "multiples": {
                "enterprise_value": mult.enterprise_value,
                "equity_value": mult.equity_value,
            },
            "football_field": ff,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run valuation engine v1")
    parser.add_argument("--input", required=True, help="Path to input payload JSON")
    parser.add_argument("--output", required=False, help="Optional path for output JSON")
    parser.add_argument(
        "--schema",
        required=False,
        help="Optional path to JSON schema for input validation",
    )

    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    output_path = Path(args.output).resolve() if args.output else None
    schema_path = Path(args.schema).resolve() if args.schema else None

    payload = _load_json(input_path)
    result = run_valuation(payload, schema_path=schema_path)

    body = json.dumps(result, indent=2)
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(body, encoding="utf-8")
        print(f"Wrote output to: {output_path}")
    else:
        print(body)


if __name__ == "__main__":
    main()
