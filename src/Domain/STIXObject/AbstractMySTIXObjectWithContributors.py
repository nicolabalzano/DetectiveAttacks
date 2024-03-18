from abc import ABC
from dataclasses import field, dataclass, fields
from typing import Tuple

from src.Domain.STIXObject.AbstractMySTIXObject import AbstractMySTIXObject
from src.Domain.STIXObject.AbstractMySTIXObjectWithName import AbstractMySTIXObjectWithName


@dataclass(eq=False, frozen=True)
class AbstractMySTIXObjectWithContributors(AbstractMySTIXObjectWithName, ABC):
    x_mitre_contributors: Tuple[str] = field(default_factory=tuple)
