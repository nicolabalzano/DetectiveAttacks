from abc import ABC
from dataclasses import dataclass, field
from typing import Dict, Tuple

from stix2.v20 import AttackPattern

from src.domain.STIXObject.AbstractMySTIXObjectWithContributors import AbstractMySTIXObjectWithContributors
from src.domain.STIXObject.MyAttackPattern import MyAttackPattern
from src.domain.STIXObject.MyRelationship import MyRelationship


@dataclass(eq=False, frozen=True)
class AbstractMySTIXObjectWithAttackPatterns(AbstractMySTIXObjectWithContributors, ABC):
    attack_patterns_and_relationships: Tuple[Dict[MyAttackPattern, tuple[MyRelationship]]] = field(
        default_factory=tuple)
