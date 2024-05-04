from dataclasses import dataclass, field

from stix2.v20 import Relationship

from src.model.domain.mySTIXObject.AbstractMySTIXObjectWithAttackPatterns import AbstractMySTIXObjectWithAttackPatterns
from src.model.domain.mySTIXObject.MyCampaign import MyCampaign
from src.model.domain.mySTIXObject.MyToolMalware import MyToolMalware


@dataclass(eq=False, frozen=True, slots=True)
class MyIntrusionSet(AbstractMySTIXObjectWithAttackPatterns):
    aliases: list[str] = field(default_factory=list)
    tool_malware_and_relationship: dict = field(default_factory=dict[MyToolMalware, Relationship])
    campaigns_and_relationship: dict = field(default_factory=dict[MyCampaign, Relationship])

    def __post_init__(self):
        object.__setattr__(self, 'x_mitre_id', '')
        for er in self.external_references:
            if '/groups/' in er.url and 'mitre' in er.source_name:
                object.__setattr__(self, 'x_mitre_id', f"{er.external_id}")
                break

    def __eq__(self, other) -> bool:
        if not isinstance(other, MyIntrusionSet):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
