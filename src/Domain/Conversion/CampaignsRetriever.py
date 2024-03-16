from stix2.v20 import Campaign

from src.Domain.Conversion.AbstractObjectWithTechniquesRetriever import AbstractObjectWithTechniquesRetriever
from src.Domain.MitreAttackData.MitreAttackData import mitre_attack_data
from src.Domain.STIXObject.MyCampaign import MyCampaign
from src.Domain.Singleton import singleton


@singleton
class CampaignsRetriever(AbstractObjectWithTechniquesRetriever):
    _KEYS_TO_DELETE: tuple = (
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

    def get_objects_using_technique_id(self, object_stix_id: str):
        return mitre_attack_data.get_campaigns_using_technique(object_stix_id)
