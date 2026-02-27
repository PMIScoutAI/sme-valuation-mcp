# SME Valuation MCP

A standard Python valuation engine for SMEs, exposed through MCP tools for Claude-compatible clients.

## What this project does
- validates input payloads with an official JSON schema
- computes valuation v1 (Projections, DCF, Multiples, Football Field)
- exposes MCP tools for agent workflows
- generates Excel baseline snapshots for numeric regression checks

## Requirements
- Windows
- Python 3.11+
- Microsoft Excel installed (required only for snapshot generation)

## Quick start
```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

## Start MCP server (one command)
With virtualenv active:
```powershell
python -m src.mcp_server
```

Helper script:
```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\start_mcp.ps1
```

## Available MCP tools
- `validate_input(payload_json: str)`
  - returns `ok` and `errors`
- `run_valuation(payload_json: str)`
  - returns valuation output JSON
- `get_model_spec()`
  - returns the content of `spec/model_spec.yaml`
- `list_scenarios()`
  - lists files in `data/samples/*.json`

## Examples
### Example 1: Run valuation from sample input
```powershell
python -m src.engine.run \
  --input data/samples/sample_inputs_1.json \
  --schema spec/schema.json \
  --output data/samples/sample_output_1.json
```

### Example 2: Validate input shape quickly
Use `data/samples/sample_inputs_invalid.json` to test validation failures:
```powershell
python -m unittest tests/test_schema_validation.py -v
```

### Example 3: Minimal MCP payload for `run_valuation`
`payload_json` content:
```json
{
  "meta": { "company_name": "SME Demo Ltd", "currency": "EUR", "years": 5 },
  "actuals": { "revenue": [12.5, 13.1, 14.0], "ebitda": [2.1, 2.3, 2.6], "nfp": 4.5 },
  "assumptions": {
    "tax_rate": 0.27,
    "wacc": 0.11,
    "terminal_growth": 0.02,
    "revenue_cagr": 0.06,
    "ebitda_margin": 0.19,
    "capex_pct_revenue": 0.04,
    "nwc_pct_revenue": 0.03
  },
  "multiples": { "ev_ebitda_multiple": 7.5, "ev_ebit_multiple": 10.0 }
}
```
Expected output sections:
- `projections.revenue|ebitda|fcf`
- `valuation.dcf.enterprise_value|equity_value`
- `valuation.multiples.enterprise_value|equity_value`
- `valuation.football_field.low|mid|high`

### Example 4: Ready-to-paste prompt for Claude (with MCP connected)
```text
Use the MCP server "sme-valuation-engine".
1) Call list_scenarios() and pick sample_inputs_1.json.
2) Load that JSON and call validate_input(payload_json).
3) If validation is ok, call run_valuation(payload_json).
4) Return a short summary with:
- DCF enterprise value and equity value
- Multiples enterprise value and equity value
- Football field low, mid, high
- 3 projected revenue values
If validation fails, show the errors clearly.
```

## Run engine without MCP
```powershell
python -m src.engine.run \
  --input data/samples/sample_inputs_1.json \
  --schema spec/schema.json \
  --output data/samples/sample_output_1.json
```

## Tests
```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

## Excel baseline snapshots
1. Configure golden cells in `spec/golden_outputs.yaml`
2. Run:
```powershell
python src/excel/compute_snapshot_xlwings.py \
  --excel SME_datapack.xlsx \
  --golden-outputs spec/golden_outputs.yaml \
  --output spec/golden_snapshots/snapshot_1.json \
  --scenario baseline \
  --inputs data/samples/sample_inputs_2.json
```

Note: some workbook sheet names are in Italian because they come from the original Excel model.

## Main project structure
- `src/engine/` valuation logic
- `src/mcp_server.py` MCP server
- `spec/model_spec.yaml` data contract
- `spec/schema.json` input validation schema
- `spec/golden_outputs.yaml` baseline cell list
- `spec/golden_snapshots/` numeric snapshots

## Connect to Claude
Register this MCP server in your client MCP config with:
`python -m src.mcp_server`

A minimal config template is in `mcp_config.example.json`.

## Publish to GitHub
Recommended flow:
1. create an empty GitHub repo (no auto README)
2. connect local remote
3. push `main`

Manual commands:
```powershell
git init
git add .
git commit -m "Initial release: SME Valuation MCP v1"
git branch -M main
git remote add origin <GITHUB_REPO_URL>
git push -u origin main
```

Automated script (create repo via API + push):
```powershell
$env:GITHUB_TOKEN="<GITHUB_PAT>"
powershell -ExecutionPolicy Bypass -File .\scripts\publish_github.ps1 -RepoName "sme-valuation-mcp" -Description "SME Valuation MCP"
```

## Current status
- valuation engine v1 ready
- schema validation ready
- Excel baseline snapshots ready
- MCP server ready (requires `mcp` package)

