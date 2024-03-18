from abc import ABC
from typing import Tuple


class AbstractContainer(ABC):

    def __init__(self, objects: Tuple):
        if not isinstance(objects, tuple):
            self._objects = tuple(objects)
        else:
            self._objects = objects

    def get_data(self):
        return self._objects

    def get_object_from_data_by_id(self, target_id: str):
        return next((obj for obj in self._objects if obj.id == target_id), None)
