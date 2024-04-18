from dataclasses import dataclass, field
from typing import List

from src.model.domain.mySTIXObject.AbstractMySTIXObjectWithAttackPatterns import AbstractMySTIXObjectWithAttackPatterns


@dataclass(eq=False, frozen=True, slots=True)
class MyCampaign(AbstractMySTIXObjectWithAttackPatterns):
    aliases: List[str] = field(default_factory=list)
    first_seen: str = ""
    last_seen: str = ""
    x_mitre_first_seen_citation: str = ""
    x_mitre_last_seen_citation: str = ""

    def __post_init__(self):
        object.__setattr__(self, 'x_mitre_id', '')
        for er in self.external_references:
            if ('/campaigns/' in er.url or '/studies/' in er.url) and 'mitre-' in er.source_name:
                object.__setattr__(self, 'x_mitre_id', f"{er.external_id}")
                break

    def set_x_mitre_domains(self, value):
        object.__setattr__(self, 'x_mitre_domains', value)

    def __eq__(self, other) -> bool:
        if not isinstance(other, MyCampaign):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
