from abc import ABC, abstractmethod
from dataclasses import field, dataclass
from datetime import datetime
from typing import List, Optional

from stix2.v20 import _DomainObject

from src.Domain.STIXObject.MyExternalReference import MyExternalReference


@dataclass
class AbstractMySTIXObject(ABC):
    type: str
    id: str
    created: datetime
    modified: datetime
    name: str
    description: str
    revoked: bool
    x_mitre_version: str
    x_mitre_attack_spec_version: str = ""
    external_references: tuple[MyExternalReference] = field(default_factory=tuple)
    x_mitre_domains: tuple[str] = field(default_factory=tuple)
    x_mitre_contributors: tuple[str] = field(default_factory=tuple)
    x_mitre_deprecated: bool = False

