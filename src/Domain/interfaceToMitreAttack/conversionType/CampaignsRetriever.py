from typing import Tuple

from stix2.v20 import Campaign

from src.domain.interfaceToMitreAttack.conversionType.AbstractObjectWithAttackPatternRetriever import _AbstractObjectWithAttackPatternsRetriever
from src.domain.interfaceToMitreAttack.mitreAttackData.MitreAttackData import mitre_attack_data
from src.domain.STIXObject.MyCampaign import MyCampaign
from src.domain.Singleton import singleton


@singleton
class CampaignsRetriever(_AbstractObjectWithAttackPatternsRetriever):

    _KEYS_TO_DELETE: Tuple = (
        'first_seen',
        'last_seen',
        'object_marking_refs',
        'x_mitre_first_seen_citation',
        'x_mitre_last_seen_citation',
        'x_mitre_modified_by_ref',
        'created_by_ref'

    )

    def __init__(self):
        super().__init__(MyCampaign, Campaign)

    def _get_all(self):
        return mitre_attack_data.get_campaigns(remove_revoked_deprecated=True)

    def get_attack_patterns_relationship_using_objects_id(self, object_stix_id: str) -> Tuple:
        return tuple(mitre_attack_data.get_techniques_used_by_campaign(object_stix_id))
