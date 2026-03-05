import sys
import os
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'stix&vulnerability')))

from src.dataProvider.container.mitreToVulnerabilityContainer.MitreToVulnerabilityContainer import MitreToVulnerabilityContainer

def test_cve(cve_id):
    print(f"Testing {cve_id}...")
    container = MitreToVulnerabilityContainer()
    try:
        results = container.get_related_attack_patterns_by_vulnerability_id(cve_id, request_mode=True)
        print(f"Results for {cve_id}:")
        for key, value in results.items():
            print(f"  {key}:")
            for pattern in value:
                print(f"    - {pattern.name} ({pattern.x_mitre_id}) [Phase: {getattr(pattern, 'kill_chain_phases', 'None')}]")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_cve("CVE-2017-0143")
