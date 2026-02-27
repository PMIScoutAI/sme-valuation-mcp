# PMI Datapack -> Standard Engine (Python) + MCP per Claude (non commerciale)

## Obiettivo
Trasformare `PMI_datapack.xlsx` in un motore standard, riproducibile e testabile:
1) Definire contratto dati: `model_spec.yaml` + `schema.json`
2) Definire golden outputs (celle chiave) e snapshot ricalcolati da Excel
3) Implementare engine Python modulare (v1: Proiezioni + DCF + Multipli + Football Field)
4) Esporre l'engine come MCP server (FastMCP)

## Vincoli / Principi
- Excel non e il runtime finale: serve solo come baseline e validazione
- Input/Output standardizzati in JSON
- Output deterministici e testati contro golden outputs
- Nessuna logica di monetizzazione

---

## Struttura cartella target
```text
repo/
  data/
    PMI_datapack.xlsx
    samples/
      sample_inputs_1.json
      sample_inputs_2.json
  spec/
    model_spec.yaml
    schema.json
    golden_outputs.yaml
    golden_snapshots/
      snapshot_1.json
      snapshot_2.json
    structure_report.json
  src/
    engine/
      __init__.py
      types.py
      projections.py
      dcf.py
      multiples.py
      football_field.py
      run.py
    excel/
      extract_structure.py
      compute_snapshot_xlwings.py
    mcp_server.py
  tests/
    test_against_golden.py
    test_schema_validation.py
  pyproject.toml  (o requirements.txt)
  README.md
```

---

## Step 0 - Setup ambiente (Windows con Excel installato)
### Requisiti
- Python 3.11+
- Microsoft Excel installato (per `xlwings`)
- Git (opzionale)

### Comandi
```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -U pip
pip install openpyxl pydantic pyyaml pandas numpy xlwings pytest mcp jsonschema
```

### Criteri di accettazione
- `python --version` >= 3.11
- `pip show mcp` e `pip show xlwings` rispondono correttamente
- L'ambiente virtuale viene attivato senza errori

---

## Step 1 - Estrarre struttura dall'Excel (analisi, non calcolo)
### Task
Creare `src/excel/extract_structure.py` che:
- apre il file con `openpyxl` (`data_only=False`)
- elenca i fogli
- conta formule per foglio
- identifica candidate output cells:
  - celle con formula
  - non referenziate da altre formule nello stesso foglio (terminali locali)
- salva un report JSON in `spec/structure_report.json`

### Output atteso
`spec/structure_report.json` con:
- `sheets`: nome, used_range approssimato, formula_count
- `candidates`: elenco celle terminali per foglio (top N)

### Criteri di accettazione
- Script eseguibile via CLI
- Report generato e versionabile
- Almeno 1 foglio con candidate output cells identificate

---

## Step 2 - Definire `model_spec.yaml` (contratto dati)
### Task
Creare `spec/model_spec.yaml` con struttura standard (inizialmente incompleta ma coerente).

### Template iniziale
```yaml
model:
  name: "pmi_datapack_standard_engine"
  version: "0.1.0"
  description: "Valuation datapack standardizzato (proiezioni + DCF + multipli + football field)."

inputs:
  meta:
    company_name: { type: string, required: false }
    currency: { type: string, required: true, default: "EUR" }
    years: { type: integer, required: true, default: 5, min: 1, max: 10 }

  actuals:
    revenue: { type: array[number], required: true, min_items: 1 }
    ebitda: { type: array[number], required: true, min_items: 1 }
    ebit: { type: array[number], required: false }
    net_income: { type: array[number], required: false }
    nfp: { type: number, required: false, description: "Net Financial Position / Net debt (convenzione segno da definire)" }

  assumptions:
    tax_rate: { type: number, required: true, default: 0.27, min: 0, max: 1 }
    wacc: { type: number, required: true, min: 0, max: 1 }
    terminal_growth: { type: number, required: true, min: -0.05, max: 0.10 }
    revenue_cagr: { type: number, required: true, min: -0.5, max: 1.0 }
    ebitda_margin: { type: number, required: true, min: -1, max: 1 }
    capex_pct_revenue: { type: number, required: true, min: -1, max: 1 }
    nwc_pct_revenue: { type: number, required: true, min: -1, max: 1 }

  multiples:
    ev_ebitda_multiple: { type: number, required: false }
    ev_ebit_multiple: { type: number, required: false }

outputs:
  projections:
    revenue: { type: array[number] }
    ebitda: { type: array[number] }
    fcf: { type: array[number] }
  valuation:
    dcf:
      enterprise_value: { type: number }
      equity_value: { type: number }
    multiples:
      enterprise_value: { type: number, required: false }
      equity_value: { type: number, required: false }
    football_field:
      low: { type: number }
      mid: { type: number }
      high: { type: number }

notes:
  sign_conventions:
    nfp: "Definire: nfp>0 = debito o cassa. Standardizzare e usare coerentemente."
```

### Criteri di accettazione
- `model_spec.yaml` valido YAML
- Convenzioni segno esplicitate in modo univoco
- Copertura minima input per far girare v1

---

## Step 3 - Generare `schema.json` da `model_spec.yaml`
### Task
Creare `spec/schema.json` (JSON Schema Draft 2020-12 o 07) allineato a `model_spec.yaml`.

### Regole pratiche
- Campi `required` coerenti
- Vincoli numerici (`min`, `max`) riflessi nello schema
- `additionalProperties: false` dove possibile

### Criteri di accettazione
- Validazione positiva su `data/samples/sample_inputs_1.json`
- Validazione negativa su almeno 1 sample volutamente invalido

---

## Step 4 - Golden outputs e snapshot Excel
### Task
1) Selezionare 20-40 celle chiave cross-sheet e salvarle in `spec/golden_outputs.yaml`
2) Implementare `src/excel/compute_snapshot_xlwings.py`:
- apre Excel via `xlwings`
- inietta input scenario in celle driver
- forza ricalcolo workbook
- legge celle target
- salva `spec/golden_snapshots/snapshot_*.json`

### Criteri di accettazione
- Snapshot ripetibili (delta entro tolleranza definita)
- Mappatura cella -> significato documentata
- Nessun riferimento hardcoded opaco senza commento

---

## Step 5 - Implementare engine Python v1
### Task
Implementare moduli:
- `src/engine/projections.py`
- `src/engine/dcf.py`
- `src/engine/multiples.py`
- `src/engine/football_field.py`
- `src/engine/run.py`

### Requisiti minimi logica
- Proiezioni: ricavi, EBITDA, FCF su `years`
- DCF: sconto flussi + terminal value
- Multipli: EV da EBITDA/EBIT e conversione a equity
- Football field: range low/mid/high combinando metodi disponibili

### Criteri di accettazione
- `run.py` produce JSON output conforme a schema
- Risultati confrontabili con golden snapshot (tolleranze per metrica)
- Separazione netta tra parsing input e logica finanziaria

---

## Step 6 - Test automatici
### Task
Creare:
- `tests/test_schema_validation.py`
- `tests/test_against_golden.py`

### Test minimi
- Validazione input/output contro schema
- Regressione numerica contro `golden_snapshots`
- Smoke test su scenario base

### Criteri di accettazione
- `pytest -q` verde
- Fallimento chiaro quando una metrica supera tolleranza

---

## Step 7 - MCP server per Claude (FastMCP)
### Task
Creare `src/mcp_server.py` con tool principali:
- `validate_input(payload_json)`
- `run_valuation(payload_json)`
- `get_model_spec()`
- `list_scenarios()`

### Requisiti
- Input/Output JSON puri
- Error handling esplicito e messaggi leggibili
- Nessuna dipendenza da Excel in runtime MCP

### Criteri di accettazione
- Server avviabile localmente
- Tool invocabili con payload di test
- Risposte coerenti con `run.py`

---

## Step 8 - Documentazione operativa
### Task
Aggiornare `README.md` con:
- setup ambiente
- comandi principali
- formato input/output
- strategia di validazione vs Excel
- limiti noti e roadmap

### Criteri di accettazione
- Un nuovo sviluppatore riesce a lanciare test e run in meno di 15 minuti

---

## Definition of Done (progetto)
- Struttura repository creata e coerente
- Contratto dati (`model_spec.yaml` + `schema.json`) valido
- Snapshot Excel prodotti e versionati
- Engine Python v1 funzionante e deterministico
- Test automatici verdi
- MCP server operativo con tool minimi
- README completo

## Rischi principali e mitigazioni
- Divergenza Excel vs Python: usare golden outputs granulari + tolleranze esplicite
- Ambiguita segni (NFP/debito/cassa): formalizzare convenzione in `model_spec.yaml` e testarla
- Fragilita automazione Excel: confinare `xlwings` al solo step snapshot, non nel runtime engine/MCP
- Scope creep: congelare v1 sulle 4 componenti (Proiezioni, DCF, Multipli, Football Field)

## Backlog post-v1 (non bloccante)
- Sensitivity table (WACC x g)
- Scenario manager multi-case
- Export report (JSON + markdown)
- CI pipeline (lint + test + regression check)
