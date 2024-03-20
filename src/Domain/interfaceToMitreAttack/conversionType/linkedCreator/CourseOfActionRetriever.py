from stix2 import CourseOfAction

from src.domain.interfaceToMitreAttack.conversionType._AbstractCreateObjectFromSTIX import _AbstractCreateObjectFromSTIX
from src.domain.MySTIXObject.MyCourseOfAction import MyCourseOfAction
from src.domain.Singleton import singleton


@singleton
class CourseOfActionRetriever(_AbstractCreateObjectFromSTIX):
    """
    _KEYS_TO_DELETE: tuple = (
        'created_by_ref',
        'object_marking_refs',
        'x_mitre_modified_by_ref'
    )
    """

    def __init__(self):
        super().__init__(MyCourseOfAction, CourseOfAction)

    def get_my_courses_of_action(self, stix_object: CourseOfAction) -> MyCourseOfAction:
        return self._get_object_from_stix(stix_object['object'])
