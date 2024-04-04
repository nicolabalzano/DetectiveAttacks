import csv
import io
import json
import os

import yaml


def read_from_json(path: str, filename: str):
    with open(f"{path}{filename}.json", "r") as file:
        return json.loads(file.read())


def save_to_json_file(json_data, filename, path):
    json_string = json.dumps(json_data, indent=4, default=str)
    __write_to_file(json_string, f"{filename}.json", path)


def __write_to_file(file_content, filename, path):
    with open(f"{path}{filename}", "w") as outfile:
        outfile.write(file_content)


def extension_check(filename: str, extension_to_check) -> bool:
    _, extension = os.path.splitext(filename)
    return extension.lower() == extension_to_check


def __format_mitre_id(mitre_id):
    # Rimuove il prefisso "T" e controlla la lunghezza del suffisso numerico
    mitre_id_suffix = mitre_id.lstrip('T')
    # Aggiunge uno zero se il suffisso ha solo tre cifre
    if len(mitre_id_suffix) == 3:
        return f"T0{mitre_id_suffix}"
    else:
        return mitre_id


# Convertire ogni riga del CSV in un dizionario, trasformando specifici valori separati da ';' in liste
def conversion_csv_string_to_json_string(csv_content: str) -> str:
    # Rimuovi il BOM (Byte Order Mark) UTF-8, se presente
    if csv_content.startswith('\ufeff'):
        csv_content = csv_content[1:]

    # Utilizza io.StringIO per simulare un file CSV basato su csv_content
    csvfile = io.StringIO(csv_content)
    reader = csv.DictReader(csvfile)

    data = []
    for row in reader:
        # Trasforma i valori in liste per ogni colonna, esclusi "CVE ID" e "Phase"
        for key, value in row.items():
            if key not in ['CVE ID', 'Phase']:
                # Dividi per ';' se presente, altrimenti crea una lista con un singolo elemento
                row[key] = [__format_mitre_id(v.strip()) for v in value.split(';') if v.strip()] if value.strip() else []
            # Per 'CVE ID' e 'Phase' lascia il valore come stringa
            if key == 'CVE ID':
                # Formatta l'ID MITRE se presente in "CVE ID"
                row[key] = __format_mitre_id(value.strip())

        data.append(row)

    # Converti i dati in una stringa JSON
    json_string = json.dumps(data, indent=4)
    return json_string
