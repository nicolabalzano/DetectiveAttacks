from abc import ABC
from dataclasses import dataclass, field
from typing import Dict, Tuple

from stix2.v20 import AttackPattern

from src.Domain.STIXObject.AbstractMySTIXObjectName import AbstractMySTIXObjectName
from src.Domain.STIXObject.MyAttackPattern import MyAttackPattern
from src.Domain.STIXObject.MyRelationship import MyRelationship


@dataclass(eq=False)
class AbstractMySTIXObjectWithAttackPatterns(AbstractMySTIXObjectName, ABC):
    attack_patterns_and_relationships: Tuple[Dict[MyAttackPattern, tuple[MyRelationship]]] = field(
        default_factory=tuple)
