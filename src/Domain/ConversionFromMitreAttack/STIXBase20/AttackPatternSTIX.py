from dataclasses import dataclass

from stix2.v20 import AttackPattern

from src.Domain.ConversionFromMitreAttack.STIXBase20.MySTIXBase20 import MySTIXBase20


@dataclass
class AttackPatternSTIX(MySTIXBase20):

    def __init__(self, obj):
        super().__init__(obj)