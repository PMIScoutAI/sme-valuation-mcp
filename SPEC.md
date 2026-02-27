# SPEC - SME Valuation Standard

Version: `1.0.0`

## 1. Purpose
Define a stable valuation contract for SMEs that can be used by MCP agents (Claude and other MCP-compatible clients).

## 2. Official Input Contract (JSON)
Root object fields:
- `meta` (required)
- `actuals` (required)
- `assumptions` (required)
- `multiples` (optional)

Reference implementation: `spec/schema.json`.

### 2.1 Minimum required fields
- `meta.currency` (string)
- `meta.years` (int, 1..10)
- `actuals.revenue` (array[number], min 1)
- `actuals.ebitda` (array[number], min 1)
- `assumptions.tax_rate` (0..1)
- `assumptions.wacc` (0..1)
- `assumptions.terminal_growth` (-0.05..0.10)
- `assumptions.revenue_cagr` (-0.5..1.0)
- `assumptions.ebitda_margin` (-1..1)
- `assumptions.capex_pct_revenue` (-1..1)
- `assumptions.nwc_pct_revenue` (-1..1)

### 2.2 Sign conventions
- `nfp_sign = positive_is_net_debt`
- `equity_value = enterprise_value - nfp`

## 3. Official Output Contract (JSON)
Root object:
- `projections`
  - `revenue: number[]`
  - `ebitda: number[]`
  - `fcf: number[]`
- `valuation`
  - `dcf.enterprise_value: number`
  - `dcf.equity_value: number`
  - `multiples.enterprise_value: number | null`
  - `multiples.equity_value: number | null`
  - `football_field.low: number`
  - `football_field.mid: number`
  - `football_field.high: number`

## 4. v1 Methodology (simplified)
- Projections:
  - revenue from CAGR on last historical value
  - EBITDA from constant margin
  - simplified FCF from NOPAT proxy, CAPEX, and NWC change
- DCF:
  - present value of explicit FCFs
  - terminal value = `FCF_(n+1)/(WACC-g)`
- Multiples:
  - EV from average of available multiples (`EV/EBITDA`, `EV/EBIT`)
- Football field:
  - range from DCF equity and multiples equity (when available)

## 5. Validation rules
- input must conform to `spec/schema.json`
- `WACC > terminal_growth` is required for DCF
- no extra properties in schema blocks (`additionalProperties: false`)

## 6. Regression baseline
- baseline Excel cells in `spec/golden_outputs.yaml`
- numeric snapshots in `spec/golden_snapshots/*.json`
- recommended check: absolute difference <= metric tolerance

## 7. Versioning
- MAJOR: breaking input/output changes
- MINOR: backward-compatible additions
- PATCH: fixes with no contract change

## 8. Standard MCP tools
The server should expose at least:
- `validate_input(payload_json: str)`
- `run_valuation(payload_json: str)`
- `get_model_spec()`
- `list_scenarios()`

## 9. Out of scope for v1
- pricing/commercial logic
- Excel dependency in MCP runtime
- mandatory AI provider integration
