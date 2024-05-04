from abc import ABC
from dataclasses import dataclass, field

from stix2.v20 import Relationship

from src.model.domain.mySTIXObject.AbstractMySTIXObjectWithContributors import AbstractMySTIXObjectWithContributors
from src.model.domain.mySTIXObject.MyAttackPattern import MyAttackPattern


@dataclass(eq=False, frozen=True, slots=True)
class AbstractMySTIXObjectWithAttackPatterns(AbstractMySTIXObjectWithContributors, ABC):
    attack_patterns_and_relationship: dict[MyAttackPattern, Relationship] = field(
        default_factory=tuple)
