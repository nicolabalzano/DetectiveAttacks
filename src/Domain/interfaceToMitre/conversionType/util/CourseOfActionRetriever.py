from stix2.v20 import CourseOfAction

from src.domain.interfaceToMitre.conversionType.stixConversionType._AbstractCreateObjectFromSTIX import _AbstractCreateObjectFromSTIX
from src.domain.business.MySTIXObject.MyCourseOfAction import MyCourseOfAction
from src.domain.Singleton import singleton


@singleton
class CourseOfActionRetriever(_AbstractCreateObjectFromSTIX):

    def __init__(self):
        super().__init__(MyCourseOfAction, CourseOfAction)

    def get_my_courses_of_action(self, stix_object: CourseOfAction) -> MyCourseOfAction:
        return self._get_object_from_stix(stix_object['object'])
