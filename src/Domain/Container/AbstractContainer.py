from abc import ABC
from typing import TypeVar, Type

from stix2.v20 import _DomainObject

from src.Domain.Conversion.AbstractObjectRetriever import AbstractObjectRetriever
from src.Domain.STIXObject.AbstractMySTIXObject import AbstractMySTIXObject

T_MY_STIX = TypeVar('T_MY_STIX', bound=AbstractMySTIXObject)
T_STIX = TypeVar('T_STIX', bound=_DomainObject)
T_RETRIEVER = TypeVar('T_RETRIEVER', bound=AbstractObjectRetriever)


class AbstractContainer(ABC):

    def __init__(self, objects: tuple):
        self.objects = objects

    def get_data(self):
        return self.objects