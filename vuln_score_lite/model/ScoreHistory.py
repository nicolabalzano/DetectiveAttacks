import json
import os
from datetime import datetime
from typing import List, Dict, Optional

class ScoreHistory:
    """Database for storing score calculation history"""
    
    def __init__(self, file_path='model/files/score_history.json'):
        self.file_path = file_path
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Create the score history file if it doesn't exist"""
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path):
            self._write_data({
                'history': [],
                'createdAt': datetime.now().isoformat()
            })
    
    def _read_data(self) -> Dict:
        """Read data from JSON file"""
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error reading score history: {e}")
            return {
                'history': [],
                'createdAt': datetime.now().isoformat()
            }
    
    def _write_data(self, data: Dict):
        """Write data to JSON file"""
        try:
            with open(self.file_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error writing score history: {e}")
    
    def add_score_entry(self, scores: Dict[int, float], excluded_cves: List[str] = None) -> bool:
        """
        Add a new score entry to history
        
        Args:
            scores: Dictionary mapping mode (0-4) to calculated score
            excluded_cves: List of CVE IDs that were excluded from calculation
        
        Returns:
            True if successfully added
        """
        data = self._read_data()
        history = data.get('history', [])
        
        entry = {
            'timestamp': datetime.now().isoformat(),
            'scores': scores,
            'excludedCves': excluded_cves or []
        }
        
        history.append(entry)
        data['history'] = history
        self._write_data(data)
        return True
    
    def get_history(self, limit: Optional[int] = None) -> List[Dict]:
        """
        Get score history entries
        
        Args:
            limit: Maximum number of entries to return (most recent first)
        
        Returns:
            List of history entries
        """
        data = self._read_data()
        history = data.get('history', [])
        
        # Return most recent entries first
        history.reverse()
        
        if limit:
            return history[:limit]
        return history
    
    def clear_history(self) -> bool:
        """Clear all history entries"""
        self._write_data({
            'history': [],
            'createdAt': datetime.now().isoformat()
        })
        return True
    
    def get_latest_scores(self) -> Optional[Dict]:
        """Get the most recent score entry"""
        data = self._read_data()
        history = data.get('history', [])
        
        if history:
            return history[-1]
        return None
