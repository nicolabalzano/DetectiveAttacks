from abc import ABC
from dataclasses import dataclass, field
from typing import Dict

from stix2.v20 import Relationship

from src.model.domain.mySTIXObject.AbstractMySTIXObjectWithContributors import AbstractMySTIXObjectWithContributors
from src.model.domain.mySTIXObject.MyAttackPattern import MyAttackPattern


@dataclass(eq=False, frozen=True, slots=True)
class AbstractMySTIXObjectWithAttackPatterns(AbstractMySTIXObjectWithContributors, ABC):
    attack_patterns_and_relationships: Dict[MyAttackPattern, Relationship] = field(
        default_factory=tuple)
