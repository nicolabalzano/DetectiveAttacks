from abc import ABC
from typing import Generic, Type

from src.Domain.ConversionFromMitreAttack.STIXBase20.MySTIXBase20 import MySTIXBase20
from src.Domain.GenericType import T_MY_STIX, T_STIX
from src.Domain.STIXObject.AbstractMySTIXObject import AbstractMySTIXObject


class AbstractCreateObjectFromSTIX(Generic[T_MY_STIX, T_STIX], ABC):
    _KEYS_TO_DELETE: tuple

    def __init__(self, my_stix_type: Type[T_MY_STIX], stix_type: Type[T_STIX]):
        # Qui controlliamo a runtime se stix_type è effettivamente una sottoclasse di MySTIXObject
        if not issubclass(my_stix_type, AbstractMySTIXObject):
            raise TypeError(f"{my_stix_type.__name__} must be a subclass of AbstractMySTIXObject")
        if not issubclass(stix_type, MySTIXBase20):
            raise TypeError(f"{stix_type.__name__} must be a subclass of _DomainObject")
        self.my_stix_type = my_stix_type
        self.stix_type = stix_type

    def __del_unused_attr(self, obj) -> dict:
        stix_object_dict = obj.__dict__
        stix_object_dict_data = stix_object_dict['_inner']

        for chiave in self._KEYS_TO_DELETE:
            stix_object_dict_data.pop(chiave, None)

        return stix_object_dict_data

    def _get_object_from_stix(self, obj) -> T_MY_STIX:
        stix_object = self.stix_type(obj)
        self.__del_unused_attr(stix_object.obj)
        my_stix_object = self.my_stix_type(**stix_object.obj)

        return my_stix_object