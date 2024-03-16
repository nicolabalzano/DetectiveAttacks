from dataclasses import dataclass, field
from typing import List

from stix2.v20 import Campaign

from src.Domain.STIXObject.AbstractMySTIXObject import AbstractMySTIXObject


@dataclass
class MyCampaign(AbstractMySTIXObject):
    aliases: tuple[str] = field(default_factory=tuple)
    # first_seen: str
    # last_seen: str
    # object_marking_refs: field(default_factory=List[str])
    # x_mitre_first_seen_citation: str
    # x_mitre_last_seen_citation: str
    # x_mitre_modified_by_ref: str
