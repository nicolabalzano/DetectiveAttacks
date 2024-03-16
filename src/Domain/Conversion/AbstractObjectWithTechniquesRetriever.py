from abc import abstractmethod, ABC
from typing import TypeVar, Type, Generic

from stix2.v20 import _DomainObject

from src.Domain.Conversion.AbstractObjectRetriever import AbstractObjectRetriever
from src.Domain.STIXObject.AbstractMySTIXObject import AbstractMySTIXObject

T_MY_STIX = TypeVar('T_MY_STIX', bound=AbstractMySTIXObject)
T_STIX = TypeVar('T_STIX', bound=_DomainObject)


class AbstractObjectWithTechniquesRetriever(AbstractObjectRetriever, Generic[T_MY_STIX, T_STIX], ABC):

    def __init__(self, my_stix_type: Type[T_MY_STIX], stix_type: Type[T_STIX]):
        super().__init__(my_stix_type, stix_type)

    @abstractmethod
    def get_objects_using_technique_id(self, object_stix_id: str):
        pass
