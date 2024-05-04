from stix2.v20 import AttackPattern

from src.model.domain.mySTIXObject.MyAttackPattern import MyAttackPattern
from src.model.interfaceToMitre.conversionType.stixConversionType._AbstractObjectRetriever import \
    _AbstractObjectRetriever
from src.model.interfaceToMitre.conversionType.util.CourseOfActionRetriever import CourseOfActionRetriever
from src.model.interfaceToMitre.conversionType.util.RelationshipRetriever import RelationshipRetriever
from src.model.interfaceToMitre.mitreData.MitreData import MITRE_ATTACK_ENTERPRISE_DATA, \
    MITRE_ATTACK_MOBILE_DATA, MITRE_ATTACK_ICS_DATA, MITRE_ATLAS_DATA
from src.model.Singleton import singleton


@singleton
class AttackPatternsRetriever(_AbstractObjectRetriever):

    def __init__(self):
        super().__init__(MyAttackPattern, AttackPattern)

    # override method to add list MyCourseOfAction (so mitigations)
    def _get_object_from_stix(self, stix_object):
        courses_of_action_dict = {}

        # create Dict[MyCourseOfAction, list[Relationship]]
        for ca in self.get_mitigation_relationship_using_object_id(stix_object['id']):
            my_relationships_value = RelationshipRetriever.get_my_relationships(ca)
            my_course_of_action_key = CourseOfActionRetriever().get_my_courses_of_action(ca)
            courses_of_action_dict[my_course_of_action_key] = my_relationships_value

        added_dict = {'courses_of_action_and_relationship': courses_of_action_dict}

        # if there isn't domain is ATLAS (because MitreAtlasData is home-made)
        if not hasattr(stix_object, 'x_mitre_domains'):
            added_dict['x_mitre_domains'] = ['atlas']

        my_stix_object = self.my_stix_type(**stix_object, **added_dict)

        return my_stix_object

    def _get_all(self):
        return (MITRE_ATTACK_ENTERPRISE_DATA.get_techniques()
                + MITRE_ATTACK_MOBILE_DATA.get_techniques()
                + MITRE_ATTACK_ICS_DATA.get_techniques()
                + MITRE_ATLAS_DATA.get_techniques())

    def get_mitigation_relationship_using_object_id(self, object_stix_id: str) -> list:
        return (MITRE_ATTACK_ENTERPRISE_DATA.get_mitigations_mitigating_technique(object_stix_id)
                + MITRE_ATTACK_MOBILE_DATA.get_mitigations_mitigating_technique(object_stix_id)
                + MITRE_ATTACK_ICS_DATA.get_mitigations_mitigating_technique(object_stix_id)
                + MITRE_ATLAS_DATA.get_mitigations_mitigating_technique(object_stix_id))
