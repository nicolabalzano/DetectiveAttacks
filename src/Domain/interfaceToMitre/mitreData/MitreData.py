from mitreattack.stix20 import MitreAttackData

from src.domain.interfaceToMitre.mitreData.mitreAttackToCVE.MitreAttackToCVEData import MitreAttackToCVEData
from src.domain.interfaceToMitre.mitreData.utils.Path import default_path, ATTACK_TO_CVE, ENTERPRISE_ATTACK, \
    MOBILE_ATTACK, ICS_ATTACK, ATLAS
from src.domain.interfaceToMitre.mitreData.mitreAtlasData.MitreAtlasData import MitreAtlasData

MITRE_ATTACK_ENTERPRISE_DATA = MitreAttackData(default_path + ENTERPRISE_ATTACK + ".json")
MITRE_ATTACK_MOBILE_DATA = MitreAttackData(default_path + MOBILE_ATTACK + ".json")
MITRE_ATTACK_ICS_DATA = MitreAttackData(default_path + ICS_ATTACK + ".json")
MITRE_ATLAS_DATA = MitreAtlasData(default_path + ATLAS + ".json")
MITRE_ATTACK_TO_CVE = MitreAttackToCVEData(default_path + ATTACK_TO_CVE + ".json")