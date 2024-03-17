from dataclasses import dataclass
from typing import Tuple

from src.Domain.ConversionFromMitreAttack.STIXBase20.MySTIXBase20 import MySTIXBase20


@dataclass
class BaseWithAttackPatterns(MySTIXBase20):
    def __init__(self, obj):
        super().__init__(obj)
        self.attack_patterns_and_relationship = None

    def set_attack_patterns_and_relationship(self, attack_patterns_and_relationship: list):
        self.attack_patterns_and_relationship = tuple(attack_patterns_and_relationship)
    