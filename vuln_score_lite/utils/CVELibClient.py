import requests
import logging
from typing import Optional, Dict, List

class CVELibClient:
    """Client to interact with cvwelib service"""
    
    def __init__(self, base_url='http://nginx:80/api/cvwelib',
                 stix_base_url='http://nginx:80/api/stix_and_vulnerability'):
        self.base_url = base_url
        self.stix_base_url = stix_base_url
    
    def get_cve(self, cve_id: str) -> Optional[Dict]:
        """Get CVE data from cvwelib"""
        try:
            response = requests.get(f"{self.base_url}/api/get_cve", params={'cveId': cve_id}, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching CVE {cve_id}: {e}")
            return None
    
    def get_cwe(self, cwe_id: str) -> Optional[Dict]:
        """Get CWE data from cvwelib"""
        try:
            response = requests.get(f"{self.base_url}/api/get_cwe", params={'cweId': cwe_id}, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching CWE {cwe_id}: {e}")
            return None

    def get_assets_for_cve(self, cve_id: str) -> List[Dict]:
        """
        Get the list of related assets (MITRE + personal) with their impact ratings for a CVE.
        Returns a list of dicts: [{'id': ..., 'name': ..., 'impact': int, 'type': 'mitre'|'personal'}, ...]
        Returns an empty list if the CVE has no related assets or the request fails.
        """
        try:
            response = requests.get(
                f"{self.stix_base_url}/get_data/get_assets_and_impacts_for_cve",
                params={'cve_id': cve_id},
                timeout=15
            )
            response.raise_for_status()
            data = response.json()
            return data if isinstance(data, list) else []
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching assets for CVE {cve_id}: {e}")
            return []
