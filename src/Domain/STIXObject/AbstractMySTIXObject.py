from abc import ABC
from dataclasses import field, dataclass, fields
from datetime import datetime
from typing import Tuple

from src.Domain.STIXObject.MyExternalReference import MyExternalReference
from src.Domain.STIXObject.convert_lists_to_tuples_in_init import convert_lists_to_tuples_in_init


@dataclass(eq=False)
class AbstractMySTIXObject(ABC):
    type: str
    id: str
    created: datetime
    modified: datetime
    description: str
    revoked: bool
    x_mitre_version: str
    x_mitre_attack_spec_version: str = ""
    external_references: Tuple[MyExternalReference] = field(default_factory=tuple)
    x_mitre_domains: Tuple[str] = field(default_factory=tuple)
    x_mitre_contributors: Tuple[str] = field(default_factory=tuple)
    x_mitre_deprecated: bool = False

