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
    
    def add_cves_bulk(self, cve_ids: list) -> dict:
        """
        Add multiple CVEs to the history and trigger score recalculation once
        
        Args:
            cve_ids: List of CVE identifiers
            
        Returns:
            Dictionary with success and error counts/messages
        """
        results = {"added": [], "failed": [], "already_present": []}
        
        to_add = []
        for cve_id in cve_ids:
            cve_id = cve_id.strip()
            if not cve_id:
                continue
                
            # Validate CVE exists in cvelib
            cve_data = self.cvelib.get_cve(cve_id)
            if not cve_data:
                logging.error(f"CVE {cve_id} not found in cvelib")
                results["failed"].append({"cveId": cve_id, "error": "Not found in cvelib"})
                continue
            
            # Check if already in DB
            existing = self.db.get_cve_list()
            if cve_id in existing:
                results["already_present"].append(cve_id)
                continue
            
            to_add.append(cve_id)
            
        # Add all valid ones to database
        for cve_id in to_add:
            if self.db.add_cve(cve_id):
                results["added"].append(cve_id)
                logging.info(f"Successfully added {cve_id} to history")
            else:
                results["failed"].append({"cveId": cve_id, "error": "Database error"})

        # Trigger automatic score recalculation once if any added
        if results["added"] and self.dashboard_controller:
            logging.info("Triggering automatic score recalculation for bulk add...")
            try:
                scores = self.dashboard_controller.calculate_and_save_all_scores([])
                logging.info(f"Scores recalculated and saved: {scores}")
            except Exception as e:
                logging.error(f"Error recalculating scores: {e}")
        
        return results
    
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
            
            # Trigger automatic score recalculation
            if self.dashboard_controller:
                logging.info("Triggering automatic score recalculation after removal...")
                try:
                    scores = self.dashboard_controller.calculate_and_save_all_scores([])
                    logging.info(f"Scores recalculated and saved: {scores}")
                except Exception as e:
                    logging.error(f"Error recalculating scores: {e}")
                    
        return result
    
    def get_all_cves(self) -> list:
        """Get all CVE IDs in history"""
        return self.db.get_cve_list()
