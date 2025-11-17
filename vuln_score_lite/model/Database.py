import json
import os
from datetime import datetime
from typing import List, Dict, Optional

class Database:
    """Simple JSON file-based database for storing CVE history"""
    
    def __init__(self, file_path='model/files/history.json'):
        self.file_path = file_path
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Create the database file if it doesn't exist"""
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path):
            self._write_data({
                'cveList': [],
                'createdAt': datetime.now().isoformat(),
                'updatedAt': datetime.now().isoformat()
            })
    
    def _read_data(self) -> Dict:
        """Read data from JSON file"""
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error reading database: {e}")
            return {
                'cveList': [],
                'createdAt': datetime.now().isoformat(),
                'updatedAt': datetime.now().isoformat()
            }
    
    def _write_data(self, data: Dict):
        """Write data to JSON file"""
        try:
            with open(self.file_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error writing database: {e}")
    
    def get_cve_list(self) -> List[str]:
        """Get the list of CVE IDs"""
        data = self._read_data()
        return data.get('cveList', [])
    
    def add_cve(self, cve_id: str) -> bool:
        """Add a CVE ID to the list (if not already present)"""
        data = self._read_data()
        cve_list = data.get('cveList', [])
        
        if cve_id not in cve_list:
            cve_list.append(cve_id)
            data['cveList'] = cve_list
            data['updatedAt'] = datetime.now().isoformat()
            self._write_data(data)
            return True
        return False
    
    def remove_cve(self, cve_id: str) -> bool:
        """Remove a CVE ID from the list"""
        data = self._read_data()
        cve_list = data.get('cveList', [])
        
        if cve_id in cve_list:
            cve_list.remove(cve_id)
            data['cveList'] = cve_list
            data['updatedAt'] = datetime.now().isoformat()
            self._write_data(data)
            return True
        return False
    
    def get_metadata(self) -> Dict:
        """Get metadata about the database"""
        data = self._read_data()
        return {
            'cveCount': len(data.get('cveList', [])),
            'createdAt': data.get('createdAt'),
            'updatedAt': data.get('updatedAt')
        }
