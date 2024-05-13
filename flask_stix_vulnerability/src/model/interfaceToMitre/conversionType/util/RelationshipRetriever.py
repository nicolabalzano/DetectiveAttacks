from typing import Dict, List

from src.model.Singleton import singleton


class RelationshipRetriever:

    @staticmethod
    def get_my_relationships(stix_object: Dict) -> List:
        list_relationships = []
        for rel_obj in stix_object['relationships']:
            list_relationships.append(rel_obj)
        return list_relationships[0]