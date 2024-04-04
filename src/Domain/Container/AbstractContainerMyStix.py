from abc import ABC
from typing import Tuple

from src.domain.container.AbstractContainer import AbstractContainer


class AbstractContainerMyStix(AbstractContainer, ABC):

    def get_object_from_data_by_id(self, target_id: str):
        return next((obj for obj in self._objects if obj.id == target_id), None)

    def get_object_from_data_by_mitre_id(self, target_id: str):
        return next((obj for obj in self._objects if obj.x_mitre_id == target_id), None)

    def get_object_from_data_by_name(self, target_name: str):
        return [obj for obj in self._objects if target_name.lower() in obj.name.lower()]