from dataclasses import dataclass
from datetime import datetime

from src.Domain.STIXObject.AbstractMySTIXObject import AbstractMySTIXObject
from src.Domain.STIXObject.convert_lists_to_tuples_in_init import convert_lists_to_tuples_in_init


@convert_lists_to_tuples_in_init
@dataclass(eq=False)
class MyRelationship(AbstractMySTIXObject):
    relationship_type: str = ""
    # object_marking_refs: List[str]
    # x_mitre_modified_by_ref: str
    # created_by_ref: str
    # source_ref: str
