from abc import ABC
from typing import Generic, Type, Dict, Tuple

from stix2.v21 import _STIXBase21

from src.domain.interfaceToMitreAttack.conversionType.GenericType import T_MY_STIX, T_STIX
from src.domain.MySTIXObject.AbstractMySTIXObject import AbstractMySTIXObject


class _AbstractCreateObjectFromSTIX(Generic[T_MY_STIX, T_STIX], ABC):
    # _KEYS_TO_DELETE: Tuple

    def __init__(self, my_stix_type: Type[T_MY_STIX], stix_type: Type[T_STIX]):
        # Qui controlliamo a runtime se stix_type è effettivamente una sottoclasse di MySTIXObject
        if not issubclass(my_stix_type, AbstractMySTIXObject):
            raise TypeError(f"{my_stix_type.__name__} must be a subclass of AbstractMySTIXObject")
        if not issubclass(stix_type, _STIXBase21):
            raise TypeError(f"{stix_type.__name__} must be a subclass of _STIXBase21")
        self.my_stix_type = my_stix_type
        self.stix_type = stix_type

    """
    def __del_unused_attr(self, obj) -> Dict:
        stix_object_dict = obj.__dict__
        stix_object_dict_data = stix_object_dict['_inner']

        for chiave in self._KEYS_TO_DELETE:
            stix_object_dict_data.pop(chiave, None)

        return stix_object_dict_data
    """

    def _get_object_from_stix(self, stix_object) -> T_MY_STIX:
        # self.__del_unused_attr(stix_object)
        my_stix_object = self.my_stix_type(**stix_object)

        return my_stix_object