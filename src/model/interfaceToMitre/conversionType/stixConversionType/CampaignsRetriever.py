from typing import List

from stix2.v20 import Campaign

from src.model.interfaceToMitre.conversionType.stixConversionType._AbstractObjectWithAttackPatternRetriever import \
    _AbstractObjectWithAttackPatternsRetriever
from src.model.interfaceToMitre.mitreData.MitreData import MITRE_ATTACK_ENTERPRISE_DATA, \
    MITRE_ATTACK_MOBILE_DATA, MITRE_ATTACK_ICS_DATA, MITRE_ATLAS_DATA
from src.model.domain.mySTIXObject.MyCampaign import MyCampaign
from src.model.Singleton import singleton


@singleton
class CampaignsRetriever(_AbstractObjectWithAttackPatternsRetriever):

    def __init__(self):
        super().__init__(MyCampaign, Campaign)

    def _get_all(self):
        return (MITRE_ATTACK_ENTERPRISE_DATA.get_campaigns()
                + MITRE_ATTACK_MOBILE_DATA.get_campaigns()
                + MITRE_ATTACK_ICS_DATA.get_campaigns()
                + MITRE_ATLAS_DATA.get_case_studies())

    # Override this method to add the x_mitre_domains attribute to the object
    def _get_object_from_stix(self, stix_object):
        my_stix_object = super()._get_object_from_stix(stix_object)
        if my_stix_object.x_mitre_domains:
            my_stix_object.set_x_mitre_domains(['atlas'])

        return my_stix_object

    def get_attack_patterns_relationship_using_objects_id(self, object_stix_id: str) -> List:
        return (MITRE_ATTACK_ENTERPRISE_DATA.get_techniques_used_by_campaign(object_stix_id)
                + MITRE_ATTACK_MOBILE_DATA.get_techniques_used_by_campaign(object_stix_id)
                + MITRE_ATTACK_ICS_DATA.get_techniques_used_by_campaign(object_stix_id)
                + MITRE_ATLAS_DATA.get_techniques_used_by_case_study(object_stix_id))
