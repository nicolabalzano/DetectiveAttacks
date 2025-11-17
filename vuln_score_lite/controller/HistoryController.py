"""Controller for managing CVE history"""

import logging
from model.Database import Database
from utils.CVELibClient import CVELibClient

class HistoryController:
    """Handles adding/removing CVEs from history"""
    
    def __init__(self, dashboard_controller=None):
        self.db = Database()
        self.cvelib = CVELibClient()
        self.dashboard_controller = dashboard_controller
    
    def add_cve(self, cve_id: str) -> bool:
        """
        Add a single CVE to the history and trigger score recalculation
        
        Args:
            cve_id: The CVE identifier (e.g., CVE-2024-12345)
            
        Returns:
            True if successfully added, False otherwise
        """
        # Validate CVE exists in cvwelib
        cve_data = self.cvelib.get_cve(cve_id)
        if not cve_data:
            logging.error(f"CVE {cve_id} not found in cvwelib")
            return False
        
        # Add to database
        result = self.db.add_cve(cve_id)
        if result:
            logging.info(f"Successfully added {cve_id} to history")
            
            # Trigger automatic score recalculation
            if self.dashboard_controller:
                logging.info("Triggering automatic score recalculation...")
                try:
                    scores = self.dashboard_controller.calculate_and_save_all_scores([])
                    logging.info(f"Scores recalculated and saved: {scores}")
                except Exception as e:
                    logging.error(f"Error recalculating scores: {e}")
        else:
            logging.info(f"CVE {cve_id} already exists in history")
        
        return True
    
    def remove_cve(self, cve_id: str) -> bool:
        """
        Remove a CVE from the history
        
        Args:
            cve_id: The CVE identifier to remove
            
        Returns:
            True if successfully removed, False otherwise
        """
        result = self.db.remove_cve(cve_id)
        if result:
            logging.info(f"Successfully removed {cve_id} from history")
        return result
    
    def get_all_cves(self) -> list:
        """Get all CVE IDs in history"""
        return self.db.get_cve_list()
