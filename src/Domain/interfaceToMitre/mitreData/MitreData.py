from mitreattack.stix20 import MitreAttackData

from src.domain.interfaceToMitre.mitreData.mitreAttackToCVE.MitreAttackToCVEData import MitreAttackToCVEData
from src.domain.interfaceToMitre.mitreData.utils.Path import default_path, ATTACK_TO_CVE, ENTERPRISE_ATTACK, \
    MOBILE_ATTACK, ICS_ATTACK, ATLAS, json_format, ATTACK_TO_CVE_SSM_HISTORY
from src.domain.interfaceToMitre.mitreData.mitreAtlasData.MitreAtlasData import MitreAtlasData

MITRE_ATTACK_ENTERPRISE_DATA = MitreAttackData(default_path + ENTERPRISE_ATTACK + json_format)
MITRE_ATTACK_MOBILE_DATA = MitreAttackData(default_path + MOBILE_ATTACK + json_format)
MITRE_ATTACK_ICS_DATA = MitreAttackData(default_path + ICS_ATTACK + json_format)
MITRE_ATLAS_DATA = MitreAtlasData(default_path + ATLAS + json_format)
MITRE_ATTACK_TO_CVE = MitreAttackToCVEData(default_path + ATTACK_TO_CVE + json_format,
                                           default_path + ATTACK_TO_CVE_SSM_HISTORY + json_format)

