from abc import ABC
from dataclasses import field, dataclass
from datetime import datetime
from typing import Tuple

from stix2.v20 import ExternalReference


@dataclass(eq=False, frozen=True, slots=True)
class AbstractMySTIXObject(ABC):
    created: datetime = field(default_factory=datetime.now)
    modified: datetime = field(default_factory=datetime.now)
    type: str = ""
    id: str = ""
    description: str = ""
    x_mitre_version: str = ""
    x_mitre_modified_by_ref: str = ""
    external_references: Tuple[ExternalReference] = field(default_factory=tuple)
    object_marking_refs: Tuple = field(default_factory=tuple)
    x_mitre_attack_spec_version: str = ""
    x_mitre_deprecated: bool = False
    revoked: bool = False
    created_by_ref: str = ""

