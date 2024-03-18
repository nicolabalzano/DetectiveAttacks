from dataclasses import dataclass

from stix2.v20 import CourseOfAction

from src.domain.STIXObject.AbstractMySTIXObjectWithName import AbstractMySTIXObjectWithName


@dataclass(eq=False, frozen=True)
class MyCourseOfAction(AbstractMySTIXObjectWithName):
    pass
    # created_by_ref: str
    # object_marking_refs: List[str]
    # x_mitre_modified_by_ref: str

    def __eq__(self, other) -> bool:
        if not isinstance(other, MyCourseOfAction):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
