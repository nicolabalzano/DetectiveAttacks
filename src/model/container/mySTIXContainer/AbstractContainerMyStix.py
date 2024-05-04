from abc import ABC

from src.model.container.mySTIXContainer._AbstractContainer import _AbstractContainer


class AbstractContainerMyStix(_AbstractContainer, ABC):

    def get_object_from_data_by_id(self, target_id: str):
        return next((obj for obj in self.get_tuple_data() if obj.id == target_id), None)

    def get_object_from_data_by_mitre_id(self, target_id: str):
        if target_id in self._objects:
            return self._objects[target_id]
        return None

    def get_object_from_data_by_name(self, target_name: str):
        return [obj for obj in self.get_tuple_data() if target_name.lower() in obj.name.lower()]