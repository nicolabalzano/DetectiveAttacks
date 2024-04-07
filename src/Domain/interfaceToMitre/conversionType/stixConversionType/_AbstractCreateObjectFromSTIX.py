from abc import ABC
from typing import Generic, Type

from src.domain.interfaceToMitre.conversionType.util.GenericType import T_MY_STIX, T_STIX
from src.domain.business.mySTIXObject.AbstractMySTIXObject import AbstractMySTIXObject


class _AbstractCreateObjectFromSTIX(Generic[T_MY_STIX, T_STIX], ABC):

    def __init__(self, my_stix_type: Type[T_MY_STIX], stix_type: Type[T_STIX]):
        # controlliamo a runtime se stix_type è effettivamente una sottoclasse di mySTIXObject
        if not issubclass(my_stix_type, AbstractMySTIXObject):
            raise TypeError(f"{my_stix_type.__name__} must be a subclass of AbstractMySTIXObject")
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
        my_stix_object = self.my_stix_type(**stix_object)

        return my_stix_object