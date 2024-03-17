from dataclasses import dataclass

from src.Domain.ConversionFromMitreAttack.STIXBase20.MySTIXBase20 import MySTIXBase20


@dataclass
class RelationshipSTIX(MySTIXBase20):

    def __init__(self, obj):
        super().__init__(obj)