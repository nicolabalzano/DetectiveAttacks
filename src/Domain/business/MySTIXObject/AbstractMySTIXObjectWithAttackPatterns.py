from abc import ABC
from dataclasses import dataclass, field
from typing import Dict

from stix2.v20 import Relationship

from src.domain.business.MySTIXObject.AbstractMySTIXObjectWithContributors import AbstractMySTIXObjectWithContributors
from src.domain.business.MySTIXObject.MyAttackPattern import MyAttackPattern


@dataclass(eq=False, frozen=True, slots=True)
class AbstractMySTIXObjectWithAttackPatterns(AbstractMySTIXObjectWithContributors, ABC):
    attack_patterns_and_relationships: Dict[MyAttackPattern, tuple[Relationship]] = field(
        default_factory=tuple)
