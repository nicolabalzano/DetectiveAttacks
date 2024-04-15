from src.model.Singleton import singleton
from src.model.container.mySTIXContainer.AbstractContainerMyStixWithAttackPatterns import AbstractContainerMyStixWithAttackPatterns


@singleton
class CampaignsContainer(AbstractContainerMyStixWithAttackPatterns):
    pass
