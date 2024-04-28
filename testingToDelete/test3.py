from pprint import pprint

from src.controller.objectRender.vulnerability import get_vulnerability_from_cve_id
from src.model.container import AttackPatternsContainer, AssetContainer, AttackToCVEContainer

print(AttackPatternsContainer().get_object_from_data_by_mitre_id('AML.CS0011'))
