# PMI Valuation MCP

Motore standard per valutazioni PMI (Python) con integrazione MCP per Claude.

## Cosa fa
- valida input JSON con schema ufficiale
- calcola valutazione v1 (Proiezioni, DCF, Multipli, Football Field)
- espone tool MCP usabili da Claude
- genera snapshot Excel baseline per regression test

## Requisiti
- Windows
- Python 3.11+
- Microsoft Excel installato (solo per snapshot Excel)

## Installazione rapida
```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

## Avvio in 1 comando
Con ambiente attivo:
```powershell
python -m src.mcp_server
```

Alternativa con script helper:
```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\start_mcp.ps1
```

## Tool MCP disponibili
- `validate_input(payload_json: str)`
  - ritorna `ok` + lista `errors`
- `run_valuation(payload_json: str)`
  - ritorna output valuation JSON
- `get_model_spec()`
  - ritorna il contenuto di `spec/model_spec.yaml`
- `list_scenarios()`
  - ritorna i file `data/samples/*.json`

## Esecuzione engine senza MCP
```powershell
python -m src.engine.run \
  --input data/samples/sample_inputs_1.json \
  --schema spec/schema.json \
  --output data/samples/sample_output_1.json
```

## Test
```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

## Snapshot Excel (baseline)
1. Configura celle golden in `spec/golden_outputs.yaml`
2. Esegui:
```powershell
python src/excel/compute_snapshot_xlwings.py \
  --excel PMI_datapack.xlsx \
  --golden-outputs spec/golden_outputs.yaml \
  --output spec/golden_snapshots/snapshot_1.json \
  --scenario baseline \
  --inputs data/samples/sample_inputs_2.json
```

## Struttura principale
- `src/engine/` logica finanziaria v1
- `src/mcp_server.py` server MCP
- `spec/model_spec.yaml` contratto dati
- `spec/schema.json` schema di validazione input
- `spec/golden_outputs.yaml` elenco celle baseline Excel
- `spec/golden_snapshots/` snapshot numerici

## Collegamento a Claude (concetto)
Devi registrare questo server MCP nella configurazione MCP del tuo client Claude, indicando il comando di avvio locale:
`python -m src.mcp_server`

Dopo il collegamento, l'agent puo selezionare e usare i tool MCP esposti.

Un esempio minimo di config e in `mcp_config.example.json`.

## Pubblicazione su GitHub
Workflow consigliato:
1. crea repository pubblico su GitHub (vuoto, senza README automatico)
2. collega il remote locale
3. push del branch principale

Comandi:
```powershell
git init
git add .
git commit -m "Initial release: PMI Valuation MCP v1"
git branch -M main
git remote add origin <URL_REPO_GITHUB>
git push -u origin main
```

Oppure script automatico (crea repo via API + push):
```powershell
$env:GITHUB_TOKEN="<PAT_GITHUB>"
powershell -ExecutionPolicy Bypass -File .\scripts\publish_github.ps1 -RepoName "pmi-valuation-mcp" -Description "PMI Valuation MCP" 
```

## Stato attuale
- engine v1 pronto
- schema/input validation pronta
- snapshot Excel pronto
- MCP server pronto (richiede dipendenza `mcp` installata)
