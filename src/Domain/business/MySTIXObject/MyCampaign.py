from dataclasses import dataclass, field
from typing import List

from src.domain.business.MySTIXObject.AbstractMySTIXObjectWithAttackPatterns import AbstractMySTIXObjectWithAttackPatterns


@dataclass(eq=False, frozen=True, slots=True)
class MyCampaign(AbstractMySTIXObjectWithAttackPatterns):
    aliases: List[str] = field(default_factory=list)
    first_seen: str = ""
    last_seen: str = ""
    x_mitre_first_seen_citation: str = ""
    x_mitre_last_seen_citation: str = ""

    def __post_init__(self):
        for er in self.external_references:
            if '/campaigns/' in er.url and 'mitre-' in er.source_name:
                object.__setattr__(self, 'x_mitre_id', f"{er.external_id}")
                break