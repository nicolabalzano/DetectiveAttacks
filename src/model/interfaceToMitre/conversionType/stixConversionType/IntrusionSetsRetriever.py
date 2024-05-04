from dataclasses import field

from stix2.v20 import IntrusionSet

from src.model.Singleton import singleton
from src.model.container import CampaignsContainer, ToolsMalwareContainer
from src.model.domain.mySTIXObject.MyIntrusionSet import MyIntrusionSet
from src.model.interfaceToMitre.conversionType.stixConversionType._AbstractObjectWithAttackPatternRetriever import \
    _AbstractObjectWithAttackPatternsRetriever
from src.model.interfaceToMitre.conversionType.util.RelationshipRetriever import RelationshipRetriever
from src.model.interfaceToMitre.mitreData.MitreData import MITRE_ATTACK_ENTERPRISE_DATA, MITRE_ATTACK_MOBILE_DATA, \
    MITRE_ATTACK_ICS_DATA


@singleton
class IntrusionSetsRetriever(_AbstractObjectWithAttackPatternsRetriever):

    def __init__(self):
        super().__init__(MyIntrusionSet, IntrusionSet)

    def _get_object_from_stix(self, stix_object):
        tool_malware_rel_dict = {}
        for dict_ in self.get_software_relationship_using_objects_id(stix_object['id']):
            tool_malware_rel_dict[ToolsMalwareContainer().get_object_from_data_by_id(dict_['object']['id'])] = RelationshipRetriever.get_my_relationships(dict_)

        campaign_rel_dict = {}
        for dict_ in self.get_campaign_relationship_using_objects_id(stix_object['id']):
            campaign_rel_dict[CampaignsContainer().get_object_from_data_by_id(dict_['object']['id'])] = RelationshipRetriever.get_my_relationships(dict_)

        added_dict = {'tool_malware_and_relationship': tool_malware_rel_dict,
                      'campaigns_and_relationship': campaign_rel_dict}

        my_stix_object = self.my_stix_type(**stix_object, **added_dict)

        return my_stix_object

    def _get_all(self):
        return (MITRE_ATTACK_ENTERPRISE_DATA.get_groups()
                + MITRE_ATTACK_MOBILE_DATA.get_groups()
                + MITRE_ATTACK_ICS_DATA.get_groups())

    def get_attack_patterns_relationship_using_objects_id(self, object_stix_id: str) -> list:
        return (MITRE_ATTACK_ENTERPRISE_DATA.get_techniques_used_by_group(object_stix_id)
                + MITRE_ATTACK_MOBILE_DATA.get_techniques_used_by_group(object_stix_id)
                + MITRE_ATTACK_ICS_DATA.get_techniques_used_by_group(object_stix_id))

    def get_software_relationship_using_objects_id(self, object_stix_id: str) -> list:
        return (MITRE_ATTACK_ENTERPRISE_DATA.get_software_used_by_group(object_stix_id)
                + MITRE_ATTACK_MOBILE_DATA.get_software_used_by_group(object_stix_id)
                + MITRE_ATTACK_ICS_DATA.get_software_used_by_group(object_stix_id))

    def get_campaign_relationship_using_objects_id(self, object_stix_id: str) -> list:
        return (MITRE_ATTACK_ENTERPRISE_DATA.get_campaigns_attributed_to_group(object_stix_id)
                + MITRE_ATTACK_MOBILE_DATA.get_campaigns_attributed_to_group(object_stix_id)
                + MITRE_ATTACK_ICS_DATA.get_campaigns_attributed_to_group(object_stix_id))