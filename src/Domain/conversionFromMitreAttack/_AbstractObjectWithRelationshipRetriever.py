from abc import ABC
from typing import Generic

from src.Domain.conversionFromMitreAttack.linkedCreator.RelationshipsRetriever import RelationshipsRetriever
from src.Domain.conversionFromMitreAttack._AbstractObjectRetriever import _AbstractObjectRetriever
from src.Domain.GenericType import T_MY_STIX, T_STIX


class _AbstractObjectWithRelationshipRetriever(_AbstractObjectRetriever, Generic[T_MY_STIX, T_STIX], ABC):
    @staticmethod
    def _get_my_relationships(stix_object: dict) -> tuple:
        return RelationshipsRetriever().get_my_relationships(stix_object)
