# SME Datapack -> Standard Engine (Python) + MCP

## Goal
Transform the source workbook (`SME_datapack.xlsx`) into a standardized, reproducible valuation engine:
1. Define data contract: `model_spec.yaml` + `schema.json`
2. Define golden outputs and Excel snapshots
3. Implement modular Python engine (v1: Projections + DCF + Multiples + Football Field)
4. Expose engine through MCP tools for Claude-compatible clients

## Principles
- Excel is baseline/validation only, not runtime
- Standard JSON input/output contract
- Deterministic outputs and regression checks
- No commercial/pricing logic in core engine

## Delivery status
- Step 1: Excel structure extraction -> done (`spec/structure_report.json`)
- Step 2: model spec -> done (`spec/model_spec.yaml`)
- Step 3: JSON schema -> done (`spec/schema.json`)
- Step 4: golden outputs and snapshots -> done (`spec/golden_outputs.yaml`, `spec/golden_snapshots/`)
- Step 5: engine v1 -> done (`src/engine/`)
- Step 6: automated tests -> done (`tests/`)
- Step 7: MCP server -> done (`src/mcp_server.py`)

## Remaining execution focus
1. Publish to GitHub and tag `v1.0.0`
2. Add CI pipeline (unit tests + schema checks)
3. Add contribution guide and release notes template

## Definition of Done
- Public repo with clear documentation
- One-command local startup for MCP server
- Stable contract and versioned standard (`SPEC.md`)
- Reproducible snapshots and passing tests

