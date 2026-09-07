# CVE2ATT&CK NIM Case Study

Questo modulo contiene il benchmark usato per confrontare le predizioni di
DetectiveAttacks con CVE2ATT&CK usando NVIDIA NIM.

Nota metodologica: CVE2ATT&CK espone categorie/nomi di tecniche, non una lista
gold di ID ATT&CK precisi. Il runner quindi mantiene come output gli ID ATT&CK
reali predetti dal modello e salva anche nome e parent technique, così il
confronto può essere fatto a livello di categoria/nome.

## Script

- `cve2attack_dataset.py`: unifica train e test di CVE2ATT&CK.
- `attack_catalog.py`: carica le tecniche Enterprise ATT&CK reali dal file STIX.
- `nvidia_nim_api.py`: client NVIDIA NIM, con chiave letta da `.env`.
- `llm_output_validation.py`: valida JSON, ID ATT&CK, duplicati e formati errati.
- `run_cve2attack_prompt_test.py`: esegue il prompt test e salva trace completi.
- `evaluate_cve2attack_predictions.py`: calcola metriche ed error analysis.

## Run salvato

Il run corrente è in:

- `results/nim_100_full/`
- `logs/nim_100_full/`

Comando usato per il caso di studio sui primi 100 sample:

```bash
python test_module/run_cve2attack_prompt_test.py \
  --sample-size 100 \
  --models mistralai/mistral-large-3-675b-instruct-2512 \
  --full-descriptions \
  --output-dir test_module/results/nim_100_full \
  --trace-dir test_module/logs/nim_100_full
```

Per ricalcolare le metriche:

```bash
python test_module/evaluate_cve2attack_predictions.py \
  --predictions test_module/results/nim_100_full/predictions_mistralai_mistral_large_3_675b_instruct_2512.jsonl
```

Metriche principali già prodotte:

- `results/nim_100_full/metrics_summary.csv`
- `results/nim_100_full/metrics_summary.json`
- `results/nim_100_full/error_analysis.csv`
- `results/nim_100_full/manual_comparison_mistralai_mistral_large_3_675b_instruct_2512.csv`

La metrica `any_hit_accuracy` considera corretta una CVE quando almeno una
tecnica predetta corrisponde a una categoria CVE2ATT&CK della stessa CVE.
