from abc import ABC, abstractmethod
from typing import Generic


from src.Domain.ConversionFromMitreAttack.AbstractCreateObjectFromSTIX import AbstractCreateObjectFromSTIX
from src.Domain.GenericType import T_MY_STIX, T_STIX


class AbstractObjectRetriever(AbstractCreateObjectFromSTIX, Generic[T_MY_STIX, T_STIX], ABC):

    def get_all_objects(self) -> tuple[T_MY_STIX, ...]:
        objs = []
        for obj in tuple(self._get_all()):
            objs.append(self._get_object_from_stix(obj))

        return tuple(objs)

    @abstractmethod
    def _get_all(self):
        pass