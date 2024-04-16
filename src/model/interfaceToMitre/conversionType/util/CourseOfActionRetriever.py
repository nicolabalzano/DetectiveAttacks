from stix2.v20 import CourseOfAction

from src.model.interfaceToMitre.conversionType.stixConversionType._AbstractCreateObjectFromSTIX import _AbstractCreateObjectFromSTIX
from src.model.domain.mySTIXObject.MyCourseOfAction import MyCourseOfAction
from src.model.Singleton import singleton


@singleton
class CourseOfActionRetriever(_AbstractCreateObjectFromSTIX):

    def __init__(self):
        super().__init__(MyCourseOfAction, CourseOfAction)

    def get_my_courses_of_action(self, stix_object: CourseOfAction) -> MyCourseOfAction:
        return self._get_object_from_stix(stix_object['object'])