"""Score calculation logic - simplified version"""

from typing import List
from utils.CVEHelper import CVEHelper

class ScoreCalculator:
    """Calculate security scores based on CVE data"""
    
    # Constants for normalization
    EXPLOITABILITY_MAX_V2 = 10.0
    EXPLOITABILITY_MAX_V3 = 3.90
    IMPACT_MAX_V2 = 10.0
    IMPACT_MAX_V3 = 6.0
    SEVERITY_MAX = 4.0
    
    SEVERITY_MAPPING = {
        "NONE": 0,
        "LOW": 1,
        "MEDIUM": 2,
        "HIGH": 3,
        "CRITICAL": 4
    }
    
    @staticmethod
    def calculate_base_score(cve_helpers: List[CVEHelper]) -> float:
        """Calculate simple average of base scores"""
        if not cve_helpers:
            return 0.0
        
        total = sum(cve.get_base_score() for cve in cve_helpers)
        return round(total / len(cve_helpers), 2)
    
    @staticmethod
    def calculate_impact_weighted_score(cve_helpers: List[CVEHelper]) -> float:
        """Calculate score weighted by impact"""
        if not cve_helpers:
            return 0.0
        
        total_weighted = 0.0
        total_weight = 0.0
        
        for cve in cve_helpers:
            base_score = cve.get_base_score()
            impact = cve.get_impact_score()
            
            # Normalize impact (max 10 for v2, 6 for v3)
            normalized_impact = impact / ScoreCalculator.IMPACT_MAX_V3
            
            total_weighted += base_score * normalized_impact
            total_weight += normalized_impact
        
        if total_weight == 0:
            return ScoreCalculator.calculate_base_score(cve_helpers)
        
        return round(total_weighted / total_weight, 2)
    
    @staticmethod
    def calculate_exploitability_weighted_score(cve_helpers: List[CVEHelper]) -> float:
        """Calculate score weighted by exploitability"""
        if not cve_helpers:
            return 0.0
        
        total_weighted = 0.0
        total_weight = 0.0
        
        for cve in cve_helpers:
            base_score = cve.get_base_score()
            exploit = cve.get_exploitability_score()
            
            # Normalize exploitability
            normalized_exploit = exploit / ScoreCalculator.EXPLOITABILITY_MAX_V3
            
            total_weighted += base_score * normalized_exploit
            total_weight += normalized_exploit
        
        if total_weight == 0:
            return ScoreCalculator.calculate_base_score(cve_helpers)
        
        return round(total_weighted / total_weight, 2)
    
    @staticmethod
    def calculate_severity_weighted_score(cve_helpers: List[CVEHelper]) -> float:
        """Calculate score weighted by severity"""
        if not cve_helpers:
            return 0.0
        
        total_weighted = 0.0
        total_weight = 0.0
        
        for cve in cve_helpers:
            base_score = cve.get_base_score()
            severity = cve.get_severity()
            severity_weight = ScoreCalculator.SEVERITY_MAPPING.get(severity, 0)
            
            total_weighted += base_score * severity_weight
            total_weight += severity_weight
        
        if total_weight == 0:
            return ScoreCalculator.calculate_base_score(cve_helpers)
        
        return round(total_weighted / total_weight, 2)
    
    @staticmethod
    def calculate_cwe_weighted_score(cve_helpers: List[CVEHelper]) -> float:
        """Calculate score weighted by number of CWEs"""
        if not cve_helpers:
            return 0.0
        
        total_weighted = 0.0
        total_weight = 0.0
        
        for cve in cve_helpers:
            base_score = cve.get_base_score()
            cwe_count = len(cve.get_cwe_ids())
            weight = cwe_count if cwe_count > 0 else 1
            
            total_weighted += base_score * weight
            total_weight += weight
        
        if total_weight == 0:
            return ScoreCalculator.calculate_base_score(cve_helpers)
        
        return round(total_weighted / total_weight, 2)

    @staticmethod
    def calculate_asset_weighted_score(cve_helpers: List[CVEHelper], assets_per_cve: dict) -> float:
        """
        Calculate score weighted by mean asset impact for each CVE.
        CVEs with no linked assets are excluded entirely from the weighted average.
        assets_per_cve: { cve_id: [{'id': ..., 'impact': int, ...}, ...] }
        """
        total_weighted = 0.0
        total_weight = 0.0

        for cve in cve_helpers:
            cve_id = cve.cve_id
            assets = assets_per_cve.get(cve_id, [])
            if not assets:
                # No linked assets — skip this CVE entirely
                continue

            impacts = [a.get('impact', 3) for a in assets]
            # normalise mean impact to 0-1 (impact scale is 1-5)
            weight = sum(impacts) / len(impacts) / 5.0

            base_score = cve.get_base_score()
            total_weighted += base_score * weight
            total_weight += weight

        if total_weight == 0:
            # No CVE had any linked asset — return 0 to signal "no data"
            return 0.0

        return round(total_weighted / total_weight, 2)

    @staticmethod
    def calculate_score_by_mode(cve_helpers: List[CVEHelper], mode: int, assets_per_cve: dict = None) -> float:
        """Calculate score based on selected mode"""
        if mode == 0:
            return ScoreCalculator.calculate_base_score(cve_helpers)
        elif mode == 1:
            return ScoreCalculator.calculate_impact_weighted_score(cve_helpers)
        elif mode == 2:
            return ScoreCalculator.calculate_exploitability_weighted_score(cve_helpers)
        elif mode == 3:
            return ScoreCalculator.calculate_severity_weighted_score(cve_helpers)
        elif mode == 4:
            return ScoreCalculator.calculate_cwe_weighted_score(cve_helpers)
        elif mode == 5:
            return ScoreCalculator.calculate_asset_weighted_score(cve_helpers, assets_per_cve or {})
        else:
            return ScoreCalculator.calculate_base_score(cve_helpers)
