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

