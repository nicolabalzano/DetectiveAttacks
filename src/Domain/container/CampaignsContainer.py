from stix2.v20 import Campaign

from src.Domain.container.AbstractContainer import AbstractContainer
from src.Domain.Singleton import singleton


@singleton
class CampaignsContainer(AbstractContainer):
    pass
