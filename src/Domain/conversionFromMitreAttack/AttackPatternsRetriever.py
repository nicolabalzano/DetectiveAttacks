from stix2.v20 import AttackPattern

from src.Domain.conversionFromMitreAttack.linkedCreator.CourseOfActionRetriever import CourseOfActionRetriever
from src.Domain.conversionFromMitreAttack._AbstractObjectWithRelationshipRetriever import _AbstractObjectWithRelationshipRetriever
from src.Domain.mitreAttackData.MitreAttackData import mitre_attack_data
from src.Domain.STIXObject.MyAttackPattern import MyAttackPattern
from src.Domain.Singleton import singleton


@singleton
class AttackPatternsRetriever(_AbstractObjectWithRelationshipRetriever):

    _KEYS_TO_DELETE: tuple = (
        'object_marking_refs',
        'x_mitre_modified_by_ref',
        'created_by_ref'
    )

    def __init__(self):
        super().__init__(MyAttackPattern, AttackPattern)

    # override method to add list MyCourseOfAction (so mitigations)
    def _get_object_from_stix(self, stix_object):
        my_courses_of_action = []
        ca_dict = {}
        for ca in tuple(mitre_attack_data.get_mitigations_mitigating_technique(stix_object['id'])):
            my_relationships_value = _AbstractObjectWithRelationshipRetriever._get_my_relationships(ca)
            my_course_of_action_key = CourseOfActionRetriever().get_my_courses_of_action(ca)
            ca_dict[my_course_of_action_key] = my_relationships_value

            my_courses_of_action.append(ca_dict)

        my_stix_object = super()._get_object_from_stix(stix_object)
        my_stix_object.__dict__['courses_of_action_and_relationship'] = my_courses_of_action
        return my_stix_object

    def _get_all(self):
        return mitre_attack_data.get_techniques(remove_revoked_deprecated=True)
