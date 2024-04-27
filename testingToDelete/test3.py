from pprint import pprint

from src.controller.objectRender.vulnerability import get_vulnerability_from_cve_id
from src.model.container import AttackPatternsContainer, AssetContainer, AttackToCVEContainer

for phase, past_ats in AttackPatternsContainer().get_probably_happened_attack_patterns_grouped_by_phase(
        AttackPatternsContainer().get_object_from_data_by_mitre_id('T1190')).items():
    for past_at, rel in past_ats.items():
        pprint(rel)
        break
    break
