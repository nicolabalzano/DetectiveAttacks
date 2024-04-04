from typing import List

from mitreattack.stix20 import Asset

from src.domain.business.MySTIXObject.MyAsset import MyAsset
from src.domain.interfaceToMitre.conversionType.stixConversionType._AbstractObjectWithAttackPatternRetriever import \
    _AbstractObjectWithAttackPatternsRetriever
from src.domain.interfaceToMitre.mitreData.MitreData import MITRE_ATTACK_ICS_DATA


class AssetRetriever(_AbstractObjectWithAttackPatternsRetriever):

    def __init__(self):
        super().__init__(MyAsset, Asset)

    def _get_all(self):
        return MITRE_ATTACK_ICS_DATA.get_assets()

    def get_attack_patterns_relationship_using_objects_id(self, object_stix_id: str) -> List:
        return MITRE_ATTACK_ICS_DATA.get_techniques_targeting_asset(object_stix_id)
