from abc import ABC, abstractmethod
from typing import Generic, Tuple

from src.domain.interfaceToMitre.conversionType.stixConversionType._AbstractCreateObjectFromSTIX import _AbstractCreateObjectFromSTIX
from src.domain.interfaceToMitre.conversionType.util.GenericType import T_MY_STIX, T_STIX


class _AbstractObjectRetriever(_AbstractCreateObjectFromSTIX, Generic[T_MY_STIX, T_STIX], ABC):

    def get_all_objects(self) -> Tuple[T_MY_STIX, ...]:
        stix_object = []
        for obj in self._get_all():
            stix_object.append(self._get_object_from_stix(obj))

        return tuple(stix_object)

    @abstractmethod
    def _get_all(self):
        pass