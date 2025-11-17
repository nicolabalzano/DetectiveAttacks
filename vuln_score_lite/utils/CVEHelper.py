"""Simplified CVE Helper for parsing CVE data from cvwelib"""

from typing import Optional, List, Tuple

class CVEHelper:
    """Helper class to extract relevant data from CVE JSON"""
    
    def __init__(self, cve_data: dict):
        self.cve_data = cve_data
        self.cve_id = cve_data.get('id', '')
        self.metrics = cve_data.get('metrics', {})
    
    def get_base_score(self) -> float:
        """Get CVSS base score (prefers v3.1, falls back to v2)"""
        try:
            if 'cvssMetricV31' in self.metrics:
                return float(self.metrics['cvssMetricV31'][0]['cvssData']['baseScore'])
            elif 'cvssMetricV2' in self.metrics:
                return float(self.metrics['cvssMetricV2'][0]['cvssData']['baseScore'])
        except (KeyError, IndexError, ValueError):
            pass
        return 0.0
    
    def get_impact_score(self) -> float:
        """Get CVSS impact score"""
        try:
            if 'cvssMetricV31' in self.metrics:
                return float(self.metrics['cvssMetricV31'][0]['impactScore'])
            elif 'cvssMetricV2' in self.metrics:
                return float(self.metrics['cvssMetricV2'][0]['impactScore'])
        except (KeyError, IndexError, ValueError):
            pass
        return 0.0
    
    def get_exploitability_score(self) -> float:
        """Get CVSS exploitability score"""
        try:
            if 'cvssMetricV31' in self.metrics:
                return float(self.metrics['cvssMetricV31'][0]['exploitabilityScore'])
            elif 'cvssMetricV2' in self.metrics:
                return float(self.metrics['cvssMetricV2'][0]['exploitabilityScore'])
        except (KeyError, IndexError, ValueError):
            pass
        return 0.0
    
    def get_severity(self) -> str:
        """Get CVSS severity rating"""
        try:
            if 'cvssMetricV31' in self.metrics:
                return self.metrics['cvssMetricV31'][0]['cvssData']['baseSeverity']
            elif 'cvssMetricV2' in self.metrics:
                severity = self.metrics['cvssMetricV2'][0]['baseSeverity']
                return severity if severity else 'NONE'
        except (KeyError, IndexError):
            pass
        return 'NONE'
    
    def get_cwe_ids(self) -> List[str]:
        """Get list of CWE IDs associated with this CVE"""
        cwe_ids = []
        try:
            weaknesses = self.cve_data.get('weaknesses', [])
            for weakness in weaknesses:
                for desc in weakness.get('description', []):
                    value = desc.get('value', '')
                    if value.startswith('CWE-'):
                        cwe_ids.append(value)
        except (KeyError, IndexError):
            pass
        return cwe_ids
    
    def get_description(self) -> str:
        """Get CVE description"""
        try:
            descriptions = self.cve_data.get('descriptions', [])
            if descriptions:
                return descriptions[0].get('value', 'No description available')
        except (KeyError, IndexError):
            pass
        return 'No description available'
    
    def get_published_date(self) -> str:
        """Get CVE published date"""
        return self.cve_data.get('published', '')
    
    def to_summary_dict(self) -> dict:
        """Convert to a summary dictionary"""
        return {
            'id': self.cve_id,
            'description': self.get_description(),
            'baseScore': self.get_base_score(),
            'impactScore': self.get_impact_score(),
            'exploitabilityScore': self.get_exploitability_score(),
            'severity': self.get_severity(),
            'cwes': self.get_cwe_ids(),
            'published': self.get_published_date()
        }
