from pprint import pprint

from src.domain.interfaceToMitreAttack.mitreAttackData.MitreAttackData import mitre_attack_data

for dt in mitre_attack_data.get_datacomponents():
    pprint(dt)