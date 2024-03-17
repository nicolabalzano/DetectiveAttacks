from abc import abstractmethod, ABC
from pprint import pprint
from typing import Type, Generic

from src.Domain.Container.AttackPatternsContainer import AttackPatternsContainer
from src.Domain.ConversionFromMitreAttack.AbstractObjectRetriever import AbstractObjectRetriever
from src.Domain.ConversionFromMitreAttack.RelationshipsRetriever import RelationshipsRetriever
from src.Domain.GenericType import T_MY_STIX, T_STIX
from src.Domain.STIXObject.MyAttackPattern import MyAttackPattern
from src.Domain.STIXObject.MyRelationship import MyRelationship


class AbstractObjectWithAttackPatternsRetriever(AbstractObjectRetriever, Generic[T_MY_STIX, T_STIX], ABC):

    def __init__(self, my_stix_type: Type[T_MY_STIX], stix_type: Type[T_STIX]):
        super().__init__(my_stix_type, stix_type)

    # ovveride method to add dict of attack_patterns and list of relationship
    def _get_object_from_stix(self, obj: T_STIX) -> T_MY_STIX:
        # try:
        list_att_rel = []
        att_rel_dict = {}
        stix_object = self.stix_type(obj)

        # TODO SICURAMENTE QUA DA PROBLEMI PERCHè NON STO RICREANDO L'OGGETTO
        for att_rel in self.get_attack_patterns_relationship_using_objects_id(stix_object.obj['id']):
            relationships_value = AbstractObjectWithAttackPatternsRetriever.__get_relationships(att_rel)
            attack_pattern_key = AbstractObjectWithAttackPatternsRetriever.__get_attack_patterns(att_rel)
            att_rel_dict[attack_pattern_key] = relationships_value
            list_att_rel.append(att_rel_dict)
            att_rel_dict = {}

        '''
        except TypeError as e:
            raise TypeError(e)
            
            raise TypeError(
                f"{AttackPatternsContainer.__name__} must initialized before, otherwise there are no AttackPatterns in data structure!")
            
        '''
        my_stix_object = super()._get_object_from_stix(stix_object.obj)
        my_stix_object.attack_patterns_and_relationships = list_att_rel
        return my_stix_object

    # get MyRelationship from object id
    @staticmethod
    def __get_relationships(stix_object: dict) -> tuple:
        return RelationshipsRetriever().get_my_relationships(stix_object)

    # get AttackPatterns from object id
    @staticmethod
    def __get_attack_patterns(stix_object: T_STIX) -> MyAttackPattern:
        return AttackPatternsContainer().get_object_from_data_by_id(stix_object['object']['id'])

    # get list of attack pattern by objects id
    @abstractmethod
    def get_attack_patterns_relationship_using_objects_id(self, object_stix_id: str) -> tuple:
        pass

    @abstractmethod
    def _get_all(self):
        pass
