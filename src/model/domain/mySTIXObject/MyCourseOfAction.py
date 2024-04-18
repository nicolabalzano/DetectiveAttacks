from dataclasses import dataclass, field

from src.model.domain.mySTIXObject.AbstractMySTIXObjectWithName import AbstractMySTIXObjectWithName


@dataclass(eq=False, frozen=True, slots=True)
class MyCourseOfAction(AbstractMySTIXObjectWithName):
    labels: field(default_factory=list) = list

    def __post_init__(self):
        for er in self.external_references:
            if '/mitigations/' in er.url and 'mitre-' in er.source_name:
                object.__setattr__(self, 'x_mitre_id', f"{er.external_id}")
                break
        object.__setattr__(self, 'x_mitre_id', '')

    def __eq__(self, other) -> bool:
        if not isinstance(other, MyCourseOfAction):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
