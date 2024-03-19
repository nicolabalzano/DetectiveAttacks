from abc import ABC
from dataclasses import field, dataclass
from datetime import datetime
from typing import Tuple


from src.domain.MySTIXObject.MyExternalReference import MyExternalReference

@dataclass(eq=False, frozen=True)
class AbstractMySTIXObject(ABC):
    type: str
    id: str
    created: datetime
    modified: datetime
    description: str
    x_mitre_version: str
    external_references: Tuple[MyExternalReference] = field(default_factory=tuple)
    x_mitre_attack_spec_version: str = ""
    x_mitre_deprecated: bool = False
    revoked: bool = False

