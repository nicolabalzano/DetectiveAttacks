# Test Module for CVE-to-ATT&CK Mapping Accuracy

Questo modulo verifica l'accuratezza del framework basato su LLM mappando le CVE ai pattern MITRE ATT&CK e confrontandoli con un dataset truth `CVE2ATT&CK-dataset.csv`.

## Requisiti 

1. L'ambiente conda `artificial_stupidity` deve essere attivo:
   ```bash
   conda activate artificial_stupidity
   ```

2. Devono essere installate le librerie di base per l'analisi e il framework:
   ```bash
   pip install pandas scikit-learn tqdm
   pip install -r ../stix&vulnerability/requirements.txt
   ```

3. Assicurati che i container per il backend (come Nginx/cvwelib API) siano in esecuzione e accessibili affinché i moduli di retrieval (`MitreToVulnerabilityContainer`) funzionino, oppure modifica temporaneamente la base URL per le API locali su `CWE.py`/`CVE.py`.

## Esecuzione

Avvia il test lanciando lo script:
```bash
python evaluate_cve_mapping.py
```

I risultati per ogni CVE, incluse metriche puntuali (Overall Precision, Recall, F1-Score) saranno mostrate a schermo e salvate all'interno di `cve_mapping_evaluation.csv`.

**Nota:** Nello script il parametro `sample_size=10` limita l'esecuzione ai primi 10, modificalo per testare tutto l'intero file CSV!
