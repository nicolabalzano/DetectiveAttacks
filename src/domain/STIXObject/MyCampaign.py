from dataclasses import dataclass, field
from typing import List, Tuple

from stix2.v20 import Campaign

from src.domain.STIXObject.AbstractMySTIXObjectWithAttackPatterns import AbstractMySTIXObjectWithAttackPatterns
from src.domain.STIXObject.convert_lists_to_tuples_in_init import convert_lists_to_tuples_in_init


@convert_lists_to_tuples_in_init
@dataclass(eq=False, frozen=True)
class MyCampaign(AbstractMySTIXObjectWithAttackPatterns):
    aliases: Tuple[str] = field(default_factory=tuple)
    # first_seen: str
    # last_seen: str
    # object_marking_refs: field(default_factory=List[str])
    # x_mitre_first_seen_citation: str
    # x_mitre_last_seen_citation: str
    # x_mitre_modified_by_ref: str
