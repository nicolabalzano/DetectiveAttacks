from abc import ABC


class AbstractContainer(ABC):

    def __init__(self, objects: tuple):
        if not isinstance(objects, tuple):
            self.objects = tuple(objects)
        else:
            self.objects = objects

    def get_data(self):
        return self.objects

    def get_object_from_data_by_id(self, target_id: str):
        return next((obj for obj in self.objects if obj.id == target_id), None)
