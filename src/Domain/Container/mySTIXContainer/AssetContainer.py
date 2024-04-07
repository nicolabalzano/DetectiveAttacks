from src.domain.Singleton import singleton
from src.domain.container.mySTIXContainer.AbstractContainerMyStixWithAttackPatterns import AbstractContainerMyStixWithAttackPatterns


@singleton
class AssetContainer(AbstractContainerMyStixWithAttackPatterns):
    pass