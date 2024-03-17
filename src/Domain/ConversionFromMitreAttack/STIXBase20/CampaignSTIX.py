from dataclasses import dataclass

from stix2.v20 import Campaign

from src.Domain.ConversionFromMitreAttack.STIXBase20.BaseWithAttackPatterns import BaseWithAttackPatterns


@dataclass
class CampaignSTIX(BaseWithAttackPatterns):
    def __init__(self, obj):
        super().__init__(obj)