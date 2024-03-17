from abc import ABC
from dataclasses import field, dataclass, fields
from typing import Tuple

from src.Domain.STIXObject.AbstractMySTIXObject import AbstractMySTIXObject


@dataclass(eq=False)
class AbstractMySTIXObjectName(AbstractMySTIXObject, ABC):
    name: str = ""
    x_mitre_attack_spec_version: str = ""
    x_mitre_domains: Tuple[str] = field(default_factory=tuple)
    x_mitre_contributors: Tuple[str] = field(default_factory=tuple)
    x_mitre_deprecated: bool = False
