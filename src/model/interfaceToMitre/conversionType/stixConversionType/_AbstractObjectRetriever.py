from abc import ABC, abstractmethod
from typing import Generic

from src.model.interfaceToMitre.conversionType.stixConversionType._AbstractCreateObjectFromSTIX import \
    _AbstractCreateObjectFromSTIX
from src.model.interfaceToMitre.conversionType.util.GenericType import T_MY_STIX, T_STIX


class _AbstractObjectRetriever(_AbstractCreateObjectFromSTIX, Generic[T_MY_STIX, T_STIX], ABC):

    def get_all_objects(self) -> dict:
        stix_object = {}
        for obj in self._get_all():
            my_stix_object = self._get_object_from_stix(obj)
            id_ = my_stix_object.x_mitre_id.strip()
            if id_ not in stix_object:
                stix_object[id_] = my_stix_object

        return stix_object

    @abstractmethod
    def _get_all(self):
        pass
