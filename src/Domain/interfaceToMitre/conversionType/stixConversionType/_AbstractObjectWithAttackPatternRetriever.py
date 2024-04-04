from abc import abstractmethod, ABC
from typing import Type, Generic, List

from src.domain.container.AttackPatternsContainer import AttackPatternsContainer
from src.domain.interfaceToMitre.conversionType.util.GenericType import T_MY_STIX, T_STIX
from src.domain.business.MySTIXObject import MyAttackPattern
from src.domain.interfaceToMitre.conversionType.stixConversionType._AbstractObjectRetriever import _AbstractObjectRetriever
from src.domain.interfaceToMitre.conversionType.util.RelationshipRetriever import RelationshipRetriever


class _AbstractObjectWithAttackPatternsRetriever(_AbstractObjectRetriever, Generic[T_MY_STIX, T_STIX], ABC):

    def __init__(self, my_stix_type: Type[T_MY_STIX], stix_type: Type[T_STIX]):
        super().__init__(my_stix_type, stix_type)

    # override method to add list of dict of attack_patterns and list of relationship
    def _get_object_from_stix(self, stix_object: T_STIX) -> T_MY_STIX:
        # TODO SICURAMENTE USARE L'ECCEZIZONE NON è LA SCELTA MIGLIORE
        # try:
        att_rel_dict = {}

        for att_rel in self.get_attack_patterns_relationship_using_objects_id(stix_object['id']):
            my_relationships_value = RelationshipRetriever.get_my_relationships(att_rel)
            my_attack_pattern_key = _AbstractObjectWithAttackPatternsRetriever.__get_my_attack_patterns(att_rel)
            att_rel_dict[my_attack_pattern_key] = my_relationships_value

        '''
        except TypeError as e:
            raise TypeError(e)
            raise TypeError(
                f"{AttackPatternsContainer.__name__} must initialized before, otherwise there are no AttackPatterns in data structure!")
        '''

        attack_patterns_and_relationships = {'attack_patterns_and_relationships': att_rel_dict}
        my_stix_object = self.my_stix_type(**stix_object, **attack_patterns_and_relationships)

        return my_stix_object

    # get AttackPatterns from object id
    @staticmethod
    def __get_my_attack_patterns(stix_object: T_STIX) -> MyAttackPattern:
        return AttackPatternsContainer().get_object_from_data_by_id(stix_object['object']['id'])

    # get list of attack pattern by objects id
    @abstractmethod
    def get_attack_patterns_relationship_using_objects_id(self, object_stix_id: str) -> List:
        pass

    @abstractmethod
    def _get_all(self):
        pass
