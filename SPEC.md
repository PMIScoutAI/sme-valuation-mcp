# SPEC - PMI Valuation Standard

Versione: `1.0.0`

## 1. Scopo
Definire un contratto stabile per valutazioni PMI riusabile da agent MCP (Claude e altri client compatibili MCP).

## 2. Input ufficiale (JSON)
Root object con campi:
- `meta` (required)
- `actuals` (required)
- `assumptions` (required)
- `multiples` (optional)

Riferimento operativo: `spec/schema.json`.

### 2.1 Campi obbligatori minimi
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

### 2.2 Convenzioni
- `nfp_sign = positive_is_net_debt`
- `equity_value = enterprise_value - nfp`

## 3. Output ufficiale (JSON)
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

## 4. Metodologia v1 (semplificata)
- Proiezioni:
  - ricavi da CAGR su ultimo storico
  - EBITDA da margine costante
  - FCF semplificato da NOPAT proxy, CAPEX e variazione NWC
- DCF:
  - PV dei FCF espliciti
  - terminal value = `FCF_(n+1)/(WACC-g)`
- Multipli:
  - EV da media dei multipli disponibili (`EV/EBITDA`, `EV/EBIT`)
- Football field:
  - range da equity DCF e equity Multipli disponibili

## 5. Regole di validazione
- input conforme a `spec/schema.json`
- `WACC > terminal_growth` obbligatorio per DCF
- nessuna proprietà extra nei blocchi schema (`additionalProperties: false`)

## 6. Baseline regressiva
- Celle Excel baseline in `spec/golden_outputs.yaml`
- Snapshot numerici in `spec/golden_snapshots/*.json`
- Confronto consigliato: differenza assoluta <= tolleranza definita per metrica

## 7. Versionamento
- MAJOR: breaking change su input/output
- MINOR: aggiunte backward-compatible
- PATCH: fix senza variazione contratto

## 8. Tool MCP standard
Il server MCP dovrebbe esporre almeno:
- `validate_input(payload_json: str)`
- `run_valuation(payload_json: str)`
- `get_model_spec()`
- `list_scenarios()`

## 9. Non obiettivi v1
- nessun pricing/commercial logic
- nessuna dipendenza Excel in runtime MCP
- nessun provider AI obbligatorio
