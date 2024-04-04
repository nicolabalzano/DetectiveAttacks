from abc import ABC


class AbstractContainer(ABC):

    def __init__(self, objects: tuple | list):
        if not isinstance(objects, tuple):
            self._objects = tuple(objects)
        else:
            self._objects = objects

    def get_data(self):
        return self._objects
