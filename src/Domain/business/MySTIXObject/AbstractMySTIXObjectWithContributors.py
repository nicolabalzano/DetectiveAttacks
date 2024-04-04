from abc import ABC
from dataclasses import field, dataclass
from typing import Tuple

from src.domain.business.MySTIXObject.AbstractMySTIXObjectWithName import AbstractMySTIXObjectWithName


@dataclass(eq=False, frozen=True, slots=True)
class AbstractMySTIXObjectWithContributors(AbstractMySTIXObjectWithName, ABC):
    x_mitre_contributors: Tuple[str] = field(default_factory=tuple)
