"""Controller for dashboard operations"""

import logging
from typing import List, Tuple, Dict
from model.Database import Database
from model.ScoreHistory import ScoreHistory
from utils.CVELibClient import CVELibClient
from utils.CVEHelper import CVEHelper
from utils.ScoreCalculator import ScoreCalculator

class DashboardController:
    """Handles dashboard data and score calculations"""
    
    def __init__(self):
        self.db = Database()
        self.score_history = ScoreHistory()
        self.cvelib = CVELibClient()
        self._pending_scores = {}  # Temporary storage for batch calculation
        self._pending_excluded = []
    
    def get_dashboard(self) -> Dict:
        """
        Get dashboard data with all CVEs
        
        Returns:
            Dictionary containing CVE list and metadata
        """
        cve_ids = self.db.get_cve_list()
        cve_data_list = []
        
        for cve_id in cve_ids:
            cve_data = self.cvelib.get_cve(cve_id)
            if cve_data:
                helper = CVEHelper(cve_data)
                cve_data_list.append(helper.to_summary_dict())
            else:
                logging.warning(f"Could not fetch data for {cve_id}")
        
        # Calculate statistics
        severity_counts = self._calculate_severity_counts(cve_data_list)
        
        return {
            'cveList': cve_data_list,
            'cveCount': len(cve_data_list),
            'severityCounts': severity_counts,
            'metadata': self.db.get_metadata()
        }
    
    def update_score(self, excluded_cve_ids: List[str], mode: int = 0, auto_save: bool = True) -> Tuple[float, List[str]]:
        """
        Calculate score excluding certain CVEs
        
        Args:
            excluded_cve_ids: List of CVE IDs to exclude from calculation
            mode: Calculation mode (0-4)
                0: Base score (simple average)
                1: Impact-weighted
                2: Exploitability-weighted
                3: Severity-weighted
                4: CWE-count weighted
            auto_save: If True, saves to history when all 5 modes are calculated
        
        Returns:
            Tuple of (score, list of checked CVE IDs)
        """
        all_cve_ids = self.db.get_cve_list()
        
        # Filter out excluded CVEs
        relevant_cve_ids = [cve_id for cve_id in all_cve_ids if cve_id not in excluded_cve_ids]
        
        if not relevant_cve_ids:
            return (0.0, excluded_cve_ids)
        
        # Fetch CVE data and create helpers
        cve_helpers = []
        for cve_id in relevant_cve_ids:
            cve_data = self.cvelib.get_cve(cve_id)
            if cve_data:
                cve_helpers.append(CVEHelper(cve_data))
        
        if not cve_helpers:
            return (0.0, excluded_cve_ids)
        
        # Calculate score based on mode
        score = ScoreCalculator.calculate_score_by_mode(cve_helpers, mode)
        
        # Store score for potential batch save
        if auto_save:
            self._pending_scores[mode] = score
            self._pending_excluded = excluded_cve_ids
            
            # If all 5 modes are calculated, save to history
            if len(self._pending_scores) == 5:
                self.score_history.add_score_entry(self._pending_scores, self._pending_excluded)
                logging.info(f"Saved score history entry with {len(self._pending_scores)} modes")
                # Reset pending data
                self._pending_scores = {}
                self._pending_excluded = []
        
        return (score, excluded_cve_ids)
    
    def calculate_and_save_all_scores(self, excluded_cve_ids: List[str] = None) -> Dict[int, float]:
        """
        Calculate all 5 score modes and save to history
        
        Args:
            excluded_cve_ids: List of CVE IDs to exclude from calculation
        
        Returns:
            Dictionary mapping mode to score
        """
        excluded_cve_ids = excluded_cve_ids or []
        scores = {}
        
        # Calculate all 5 modes
        for mode in range(5):
            score, _ = self.update_score(excluded_cve_ids, mode)
            scores[mode] = score
        
        # Save to history
        self.score_history.add_score_entry(scores, excluded_cve_ids)
        
        return scores
    
    def get_score_history(self, limit: int = None) -> List[Dict]:
        """
        Get score history
        
        Args:
            limit: Maximum number of entries to return
        
        Returns:
            List of history entries with timestamp and scores
        """
        return self.score_history.get_history(limit)
    
    def _calculate_severity_counts(self, cve_data_list: List[Dict]) -> Dict:
        """Calculate count of each severity level"""
        counts = {
            'CRITICAL': 0,
            'HIGH': 0,
            'MEDIUM': 0,
            'LOW': 0,
            'NONE': 0
        }
        
        for cve in cve_data_list:
            severity = cve.get('severity', 'NONE')
            if severity in counts:
                counts[severity] += 1
        
        return counts
