import requests
import logging
from typing import Optional, Dict

class CVELibClient:
    """Client to interact with cvwelib service"""
    
    def __init__(self, base_url='http://nginx:80/api/cvwelib'):
        self.base_url = base_url
    
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
