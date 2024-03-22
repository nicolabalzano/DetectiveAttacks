from abc import ABC
from typing import Generic, Tuple, Dict

from src.domain.interfaceToMitreAttack.conversionType.linkedCreator.RelationshipsRetriever import RelationshipsRetriever
from src.domain.interfaceToMitreAttack.conversionType._AbstractObjectRetriever import _AbstractObjectRetriever
from src.domain.interfaceToMitreAttack.conversionType.GenericType import T_MY_STIX, T_STIX


class _AbstractObjectWithRelationshipRetriever(_AbstractObjectRetriever, Generic[T_MY_STIX, T_STIX], ABC):

    def _get_my_relationships(self, stix_object: Dict) -> Tuple:
        return RelationshipsRetriever().get_my_relationships(stix_object)
