from pprint import pprint

from src.controller.objectRender.util import format_kill_chain_phases
from src.controller.objectRender.vulnerability import get_vulnerability_from_cve_id
from src.model.container import AttackPatternsContainer, AssetContainer, AttackToCVEContainer
from src.model.domain.AttackPhase import AttackPhase

at = AttackPatternsContainer().get_object_from_data_by_mitre_id('T1078.002')

print('\nPast')
for key, value in AttackPatternsContainer().get_probably_happened_attack_patterns_grouped_by_phase(at).items():
    print("    ", key, len(value))
print(len(AttackPatternsContainer().get_probably_happened_attack_patterns_grouped_by_CKCPhase(at)['Installation']))

print('\nFuture')
for key, value in AttackPatternsContainer().get_futured_attack_patterns_grouped_by_phase(at).items():
    print("    ", key, len(value))
print(len(AttackPatternsContainer().get_futured_attack_patterns_grouped_by_CKCPhase(at)['Installation']))

