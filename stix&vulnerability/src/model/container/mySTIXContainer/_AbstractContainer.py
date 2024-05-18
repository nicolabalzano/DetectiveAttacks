from abc import ABC

from src.model.domain.mySTIXObject.MyCampaign import MyCampaign


class _AbstractContainer(ABC):

    def __init__(self, objects: dict):
        self._objects = objects

    def get_tuple_data(self):
        return tuple(self._objects.values())
