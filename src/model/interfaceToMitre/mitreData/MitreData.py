from mitreattack.stix20 import MitreAttackData

from src.model.interfaceToMitre.mitreData.attackToVulnerability.MitreToVulnerabilityData import \
    MitreToVulnerabilityData
from src.model.interfaceToMitre.mitreData.utils.Path import default_path, MITRE_TO_CVE, MITRE_TO_CWE, ENTERPRISE_ATTACK, \
    MOBILE_ATTACK, ICS_ATTACK, ATLAS, json_format, MITRE_TO_CVE_SSM_HISTORY, MITRE_TO_CWE_SSM_HISTORY
from src.model.interfaceToMitre.mitreData.mitreAtlasData.MitreAtlasData import MitreAtlasData

MITRE_ATTACK_ENTERPRISE_DATA = MitreAttackData(default_path + ENTERPRISE_ATTACK + json_format)
MITRE_ATTACK_MOBILE_DATA = MitreAttackData(default_path + MOBILE_ATTACK + json_format)
MITRE_ATTACK_ICS_DATA = MitreAttackData(default_path + ICS_ATTACK + json_format)
MITRE_ATLAS_DATA = MitreAtlasData(default_path + ATLAS + json_format)
MITRE_TO_CVE_DATA = MitreToVulnerabilityData(default_path + MITRE_TO_CVE + json_format,
                                             default_path + MITRE_TO_CVE_SSM_HISTORY + json_format)
MITRE_TO_CWE_DATA = MitreToVulnerabilityData(default_path + MITRE_TO_CWE + json_format,
                                             default_path + MITRE_TO_CWE_SSM_HISTORY + json_format)
