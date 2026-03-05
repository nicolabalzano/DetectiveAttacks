import sys
import os
import pandas as pd
import numpy as np
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
from tqdm import tqdm

# Add the stix&vulnerability folder to the search path for imports
framework_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'stix&vulnerability'))
sys.path.append(framework_path)

from src.dataProvider.container.mitreToVulnerabilityContainer.MitreToVulnerabilityContainer import MitreToVulnerabilityContainer

def format_attack_pattern_to_column(ap):
    """
    Converts a STIX Attack Pattern object into the column name format used in the CSV.
    Example: 'reconnaissance' and 'Active Scanning' -> 'Reconnaissance - Active Scanning'
    """
    columns = []
    if not hasattr(ap, 'kill_chain_phases'):
        return columns
    
    for phase in ap.kill_chain_phases:
        phase_name = phase.phase_name
        # Capitalize each word in the phase name
        tactic_parts = phase_name.split('-')
        tactic = ' '.join(part.capitalize() for part in tactic_parts)
        
        # specific hardcoded fix for 'Command And Control'
        if tactic.lower() == 'command and control':
            tactic = 'Command And Control'
            
        columns.append(f"{tactic} - {ap.name}")
    return columns

def evaluate_framework(csv_path, output_path="evaluation_results.csv", sample_size=None, use_llm=True):
    print(f"Loading dataset {csv_path}...")
    df = pd.read_csv(csv_path)
    
    # If sample size is provided, restrict the evaluation to speed up testing
    if sample_size and sample_size > 0:
        df = df.head(sample_size)
    
    # Extract only technique columns
    technique_columns = [col for col in df.columns if ' - ' in col]
    
    print("Initializing framework container...")
    container = MitreToVulnerabilityContainer()
    
    all_y_true = []
    all_y_pred = []
    
    results_records = []
    
    # Evaluate each CVE in the dataset
    for index, row in tqdm(df.iterrows(), total=len(df), desc="Evaluating CVEs"):
        # The CSV contains underscores (CVE_2019_11886) but the regex checker expects hyphens (CVE-2019-11886)
        cve_id = row['ID'].replace('_', '-')
        
        # Ground truth techniques (where column value is 1)
        true_techniques = set()
        for col in technique_columns:
            if row[col] == 1:
                true_techniques.add(col)
                
        pred_techniques = set()
        
        # Get framework prediction
        try:
            # request_mode=use_llm triggers the LLM/CAPEC generation if mapping doesn't exist
            # Note: During some tests this might hit API limit or leak errors depending on API key
            mapping_results = container.get_related_attack_patterns_by_vulnerability_id(cve_id, request_mode=use_llm)
            
            # Combine all attack patterns from different mapping phases
            for mapping_type, patterns in mapping_results.items():
                if mapping_type == 'relationship_source':
                    continue
                for ap in patterns:
                    mapped_cols = format_attack_pattern_to_column(ap)
                    for mc in mapped_cols:
                        if mc in technique_columns:
                            pred_techniques.add(mc)
                            
        except Exception as e:
            print(f"\nError processing {cve_id} (API failure or missing container): {e}")
            # In case of API failure, we might want to either count as 0 predicted or skip
            # Skipping is usually more representative if the framework outright crashed for this row.
            continue
            
        # Create binary vectors for this row
        y_true_row = [1 if col in true_techniques else 0 for col in technique_columns]
        y_pred_row = [1 if col in pred_techniques else 0 for col in technique_columns]
        
        all_y_true.extend(y_true_row)
        all_y_pred.extend(y_pred_row)
        
        results_records.append({
            'ID': cve_id,
            'True_Count': len(true_techniques),
            'Pred_Count': len(pred_techniques),
            'True_Techniques': "; ".join(true_techniques),
            'Pred_Techniques': "; ".join(pred_techniques)
        })

    # Mostriamo a schermo i risultati per ogni CVE
    print("\n\n" + "="*60)
    print("          CVE PREDICTIONS VS GROUND TRUTH")
    print("="*60)
    for record in results_records:
        # Funzione helper veloce per mostrare solo la tecnica senza la tattica per il print
        def clean_technique_list(tech_string):
            if not tech_string:
                return "N/A"
            techs = tech_string.split("; ")
            cleaned = [t.split(" - ", 1)[-1] if " - " in t else t for t in techs]
            return "; ".join(cleaned)

        print(f"\n[+] CVE ID: {record['ID']}")
        print(f"    Expected (Dataset)   : {clean_technique_list(record['True_Techniques'])}")
        print(f"    Predicted (Framework): {clean_technique_list(record['Pred_Techniques'])}")
    print("="*60 + "\n")

    # Metrics computation
    if len(all_y_true) > 0:
        precision = precision_score(all_y_true, all_y_pred, zero_division=0)
        recall = recall_score(all_y_true, all_y_pred, zero_division=0)
        f1 = f1_score(all_y_true, all_y_pred, zero_division=0)
        accuracy = accuracy_score(all_y_true, all_y_pred)
        
        print("\n=== Evaluation Results ===")
        print(f"Total CVEs evaluated : {len(results_records)}")
        print(f"Overall Accuracy     : {accuracy:.4f}")
        print(f"Overall Precision    : {precision:.4f}")
        print(f"Overall Recall       : {recall:.4f}")
        print(f"Overall F1 Score     : {f1:.4f}")
        
        pd.DataFrame(results_records).to_csv(output_path, index=False)
        print(f"Per-CVE details saved to {output_path}")
    else:
        print("\nNo valid evaluations were completed. Checking logs for API or connection errors.")

if __name__ == "__main__":
    dataset_path = "/home/alocin/Documents/research/DetectiveAttacks/CVE2ATT&CK-dataset.csv"
    output_report = os.path.join(os.path.dirname(__file__), "cve_mapping_evaluation.csv")
    
    # Setting sample_size=10 for testing purposes, remove or set to None for full run
    evaluate_framework(dataset_path, output_path=output_report, sample_size=10, use_llm=True)
