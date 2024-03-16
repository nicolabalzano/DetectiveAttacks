from stix2.v20 import Tool

from src.Domain.Container.AbstractContainer import AbstractContainer
from src.Domain.Conversion.ToolsRetriever import ToolsRetriever
from src.Domain.STIXObject.MyTool import MyTool
from src.Domain.Singleton import singleton


@singleton
class ToolsContainer(AbstractContainer):
    pass