from __future__ import annotations

import argparse
import json
from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml


def _json_safe(value: Any) -> Any:
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, (list, tuple)):
        return [_json_safe(v) for v in value]
    if isinstance(value, dict):
        return {str(k): _json_safe(v) for k, v in value.items()}
    return value


def _load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8-sig"))


def _load_json(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {}
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _apply_inputs(workbook, scenario_inputs: dict[str, Any]) -> None:
    # Expected shape:
    # {
    #   "Sheet Name": {
    #      "C10": 123,
    #      "D10": 456
    #   }
    # }
    for sheet_name, cells in scenario_inputs.items():
        sheet = workbook.sheets[sheet_name]
        for addr, value in cells.items():
            sheet.range(addr).value = value


def compute_snapshot(
    excel_path: Path,
    golden_outputs_path: Path,
    output_path: Path,
    scenario_name: str,
    scenario_inputs_path: Path | None = None,
) -> Path:
    try:
        import xlwings as xw
    except Exception as exc:  # pragma: no cover
        raise RuntimeError("xlwings is required. Install with: pip install xlwings") from exc

    spec = _load_yaml(golden_outputs_path)
    outputs = spec.get("outputs", [])
    if not outputs:
        raise ValueError("golden_outputs.yaml has no 'outputs' entries.")

    scenario_inputs = _load_json(scenario_inputs_path)

    app = xw.App(visible=False, add_book=False)
    app.display_alerts = False
    app.screen_updating = False

    snapshot_values: list[dict[str, Any]] = []
    try:
        wb = app.books.open(str(excel_path))
        try:
            if scenario_inputs:
                _apply_inputs(wb, scenario_inputs)

            app.calculate()

            for item in outputs:
                key = item["key"]
                sheet_name = item["sheet"]
                cell_addr = item["cell"]
                description = item.get("description", "")

                value = wb.sheets[sheet_name].range(cell_addr).value
                snapshot_values.append(
                    {
                        "key": key,
                        "sheet": sheet_name,
                        "cell": cell_addr,
                        "description": description,
                        "value": _json_safe(value),
                    }
                )
        finally:
            wb.close()
    finally:
        app.quit()

    body = {
        "scenario": scenario_name,
        "source_workbook": str(excel_path),
        "golden_outputs": str(golden_outputs_path),
        "values": snapshot_values,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(body, indent=2), encoding="utf-8")
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute Excel golden snapshot via xlwings")
    parser.add_argument("--excel", required=True, help="Path to source workbook")
    parser.add_argument(
        "--golden-outputs",
        default="spec/golden_outputs.yaml",
        help="Path to golden_outputs.yaml",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output snapshot JSON path (e.g. spec/golden_snapshots/snapshot_1.json)",
    )
    parser.add_argument("--scenario", default="baseline", help="Scenario name")
    parser.add_argument(
        "--inputs",
        default=None,
        help="Optional JSON file with input cell overrides by sheet",
    )
    args = parser.parse_args()

    out = compute_snapshot(
        excel_path=Path(args.excel).resolve(),
        golden_outputs_path=Path(args.golden_outputs).resolve(),
        output_path=Path(args.output).resolve(),
        scenario_name=args.scenario,
        scenario_inputs_path=Path(args.inputs).resolve() if args.inputs else None,
    )
    print(f"Snapshot written to: {out}")


if __name__ == "__main__":
    main()
