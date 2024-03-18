from stix2.v20 import Relationship

from src.Domain.conversionFromMitreAttack._AbstractCreateObjectFromSTIX import _AbstractCreateObjectFromSTIX
from src.Domain.STIXObject.MyRelationship import MyRelationship
from src.Domain.Singleton import singleton


@singleton
class RelationshipsRetriever(_AbstractCreateObjectFromSTIX):

    _KEYS_TO_DELETE: tuple = (
        'object_marking_refs',
        'x_mitre_modified_by_ref',
        'created_by_ref',
        'target_ref'
    )

    def __init__(self):
        super().__init__(MyRelationship, Relationship)

    # get list of MyRelationship object
    def get_my_relationships(self, stix_object: dict) -> tuple:
        list_relationships = []
        for rel_obj in stix_object['relationships']:
            list_relationships.append(self._get_object_from_stix(rel_obj))
        return tuple(list_relationships)