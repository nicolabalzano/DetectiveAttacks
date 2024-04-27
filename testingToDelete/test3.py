from pprint import pprint

from src.controller.objectRender.vulnerability import get_vulnerability_from_cve_id
from src.model.container import AttackPatternsContainer, AssetContainer, AttackToCVEContainer

for key, at in AttackToCVEContainer().get_attack_pattern_by_cve_id("CVE-2019-15243").items():
    print(key, len(at), type(at))


pprint(get_vulnerability_from_cve_id("CVE-2019-15243"))
