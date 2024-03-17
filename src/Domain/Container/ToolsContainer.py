from stix2.v20 import Tool

from src.Domain.Container.AbstractContainer import AbstractContainer
from src.Domain.ConversionFromMitreAttack.ToolsRetriever import ToolsRetriever
from src.Domain.STIXObject.MyToolMalware import MyToolMalware
from src.Domain.Singleton import singleton


@singleton
class ToolsContainer(AbstractContainer):
    pass