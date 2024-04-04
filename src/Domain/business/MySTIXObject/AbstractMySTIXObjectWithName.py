from abc import ABC
from dataclasses import dataclass, field

from src.domain.business.MySTIXObject.AbstractMySTIXObject import AbstractMySTIXObject


@dataclass(eq=False, frozen=True, slots=True)
class AbstractMySTIXObjectWithName(AbstractMySTIXObject, ABC):
    name: str = ""
    x_mitre_domains: tuple[str] = field(default_factory=tuple)
    x_mitre_id: str = field(default="", init=False)
