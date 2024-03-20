from dataclasses import dataclass

from src.domain.MySTIXObject.AbstractMySTIXObject import AbstractMySTIXObject
from src.domain.MySTIXObject.convert_lists_to_tuples_in_init import convert_lists_to_tuples_in_init


@convert_lists_to_tuples_in_init
@dataclass(eq=False, frozen=True)
class MyRelationship(AbstractMySTIXObject):
    relationship_type: str = ""
    source_ref: str = ""
    target_ref: str = ""