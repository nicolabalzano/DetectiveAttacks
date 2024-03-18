from dataclasses import dataclass

from src.Domain.STIXObject.AbstractMySTIXObject import AbstractMySTIXObject
from src.Domain.STIXObject.convert_lists_to_tuples_in_init import convert_lists_to_tuples_in_init


@convert_lists_to_tuples_in_init
@dataclass(eq=False, frozen=True)
class MyRelationship(AbstractMySTIXObject):
    relationship_type: str = ""
    source_ref: str = ""
    # object_marking_refs: List[str]
    # x_mitre_modified_by_ref: str
    # created_by_ref: str
