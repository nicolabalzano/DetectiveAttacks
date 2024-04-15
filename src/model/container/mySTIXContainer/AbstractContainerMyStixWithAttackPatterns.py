from abc import ABC

from src.model.container.mySTIXContainer.AbstractContainerMyStix import AbstractContainerMyStix


class AbstractContainerMyStixWithAttackPatterns(AbstractContainerMyStix, ABC):
    
    def __init__(self, objects: tuple):
        super().__init__(objects)

    def get_related_attack_patterns_by_attack_pattern_id(self, attack_pattern_id: str) -> dict:
        attack_patterns_rel = {}

        # for every object in _objects
        for obj in self._objects:
            # for dict in attack_patterns_and_relationships tuple
            for key in obj.attack_patterns_and_relationships:
                # if it's related, save in set all key of this dict
                if attack_pattern_id == key.id:
                    attack_patterns_rel.update(obj.attack_patterns_and_relationships)
        return attack_patterns_rel
