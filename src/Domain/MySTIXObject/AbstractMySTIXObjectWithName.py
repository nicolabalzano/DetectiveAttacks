from abc import ABC
from dataclasses import dataclass, field
from typing import Tuple

from src.domain.MySTIXObject.AbstractMySTIXObject import AbstractMySTIXObject


@dataclass(eq=False, frozen=True)
class AbstractMySTIXObjectWithName(AbstractMySTIXObject, ABC):
    name: str = ""
    x_mitre_domains: Tuple[str] = field(default_factory=tuple)
