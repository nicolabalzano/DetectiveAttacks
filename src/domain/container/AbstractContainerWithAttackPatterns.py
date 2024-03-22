from abc import ABC
from typing import Tuple, Set

from src.domain.MySTIXObject.MyAttackPattern import MyAttackPattern
from src.domain.container.AbstractContainer import AbstractContainer


class AbstractContainerWithAttackPatterns(AbstractContainer, ABC):
    
    def __init__(self, objects: Tuple):
        super().__init__(objects)

    def get_related_attack_patterns_by_attack_pattern(self, attack_pattern_id: str) -> Set:
        attack_patterns = set()

        # for every object in _objects
        for obj in self._objects:
            # for dict in attack_patterns_and_relationships tuple
            for obj_dict in obj.attack_patterns_and_relationships:
                # for every key in dict
                for key in obj_dict:
                    # if it's related, save in set all key of this dict
                    if attack_pattern_id == key.id:
                        # attack_patterns.add(key)
                        attack_patterns.update(self.__get_related_attack_patterns_by_object(obj.attack_patterns_and_relationships))

        return attack_patterns

    def __get_related_attack_patterns_by_object(self, related_objs: Tuple) -> Set:
        attack_patterns = set()

        for related_obj_dict in related_objs:
            for key in related_obj_dict:
                attack_patterns.add(key)

        return attack_patterns