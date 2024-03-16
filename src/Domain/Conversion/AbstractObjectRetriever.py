from abc import ABC, abstractmethod
from typing import Generic, Type, TypeVar

from stix2.v20 import _DomainObject

from src.Domain.STIXObject.AbstractMySTIXObject import AbstractMySTIXObject

T_MY_STIX = TypeVar('T_MY_STIX', bound=AbstractMySTIXObject)
T_STIX = TypeVar('T_STIX', bound=_DomainObject)


class AbstractObjectRetriever(Generic[T_MY_STIX, T_STIX], ABC):
    _KEYS_TO_DELETE: tuple

    def __init__(self, my_stix_type: Type[T_MY_STIX], stix_type: Type[T_STIX]):
        # Qui controlliamo a runtime se stix_type è effettivamente una sottoclasse di MySTIXObject
        if not issubclass(my_stix_type, AbstractMySTIXObject):
            raise TypeError(f"{my_stix_type.__name__} must be a subclass of MySTIXObject")
        if not issubclass(stix_type, _DomainObject):
            raise TypeError(f"{stix_type.__name__} must be a subclass of _DomainObject")
        self.my_stix_type = my_stix_type
        self.stix_type = stix_type

    # inizializza oggetti MyTool
    def get_all_objects(self) -> list[T_MY_STIX]:
        objs = []
        for obj in self._get_all():
            objs.append(self._create_object_from_stix(obj))

        return objs

    # get list of objects by technique id
    def get_object_by_technique_id(self, object_stix_id: str) -> list:
        list_my_objects = []
        list_objects = self._get_objects_using_technique_id(object_stix_id)
        for obj in list_objects:
            list_my_objects.append(self._create_object_from_stix(obj['object']))

        return list_my_objects

    def __del_unused_attr(self, stix_object: T_STIX) -> dict:
        stix_object_dict = stix_object.__dict__
        stix_object_dict_data = stix_object_dict['_inner']

        for chiave in self._KEYS_TO_DELETE:
            stix_object_dict_data.pop(chiave, None)

        return stix_object_dict_data

    def _create_object_from_stix(self, stix_object: T_STIX) -> T_MY_STIX:
        self.__del_unused_attr(stix_object)
        my_stix_object = self.my_stix_type(**stix_object)

        return my_stix_object

    @abstractmethod
    def _get_all(self):
        pass


