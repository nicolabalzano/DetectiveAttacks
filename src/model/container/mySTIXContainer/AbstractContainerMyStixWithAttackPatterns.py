from abc import ABC

from src.model.container.mySTIXContainer.AbstractContainerMyStix import AbstractContainerMyStix


class AbstractContainerMyStixWithAttackPatterns(AbstractContainerMyStix, ABC):
    
    def __init__(self, objects: dict):
        super().__init__(objects)

    def get_objects_related_by_attack_pattern_id(self, attack_pattern_id: str) -> dict:
        """
        Get the object using the attack pattern id
        :param attack_pattern_id: the attack pattern id
        :return: the list of objects
        """
        obj_rel = {}

        # for every object in _objects
        for obj in self.get_tuple_data():
            # for dict in attack_patterns_and_relationships tuple
            for key in obj.attack_patterns_and_relationship:
                # if it's related, save in set all key of this dict
                if attack_pattern_id == key.id:
                    obj_rel[obj] = obj.attack_patterns_and_relationship[key]
        return obj_rel

    def get_related_attack_patterns_by_attack_pattern_id(self, attack_pattern_id: str) -> dict:
        attack_patterns_rel = {}

        # for every object in _objects
        for obj in self.get_tuple_data():
            # for dict in attack_patterns_and_relationships tuple
            for key in obj.attack_patterns_and_relationship:
                # if it's related, save in set all key of this dict
                if attack_pattern_id == key.id:
                    attack_patterns_rel.update(obj.attack_patterns_and_relationship)
        return attack_patterns_rel
