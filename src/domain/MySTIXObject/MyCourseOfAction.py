from dataclasses import dataclass

from stix2.v20 import CourseOfAction

from src.domain.MySTIXObject.AbstractMySTIXObjectWithName import AbstractMySTIXObjectWithName


@dataclass(eq=False, frozen=True)
class MyCourseOfAction(AbstractMySTIXObjectWithName):

    def __eq__(self, other) -> bool:
        if not isinstance(other, MyCourseOfAction):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
