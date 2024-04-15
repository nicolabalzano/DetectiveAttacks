from dataclasses import dataclass, field

from src.model.domain.mySTIXObject.AbstractMySTIXObjectWithAttackPatterns import AbstractMySTIXObjectWithAttackPatterns


@dataclass(eq=False, frozen=True, slots=True)
class MyAsset(AbstractMySTIXObjectWithAttackPatterns):
    x_mitre_platforms: list[str] = field(default_factory=list)
    x_mitre_sectors: list[str] = field(default_factory=list)
    spec_version: str = ""
    x_mitre_related_assets: list = field(default_factory=list)

    def __post_init__(self):
        for er in self.external_references:
            if '/assets/' in er.url and 'mitre-' in er.source_name:
                object.__setattr__(self, 'x_mitre_id', f"{er.external_id}")
                break

    def __eq__(self, other) -> bool:
        if not isinstance(other, MyAsset):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
