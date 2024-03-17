
from src.Domain.ConversionFromMitreAttack.AbstractCreateObjectFromSTIX import AbstractCreateObjectFromSTIX
from src.Domain.ConversionFromMitreAttack.AbstractObjectRetriever import AbstractObjectRetriever
from src.Domain.ConversionFromMitreAttack.STIXBase20.RelationshipSTIX import RelationshipSTIX
from src.Domain.MitreAttackData.MitreAttackData import mitre_attack_data
from src.Domain.STIXObject.MyRelationship import MyRelationship
from src.Domain.Singleton import singleton


@singleton
class RelationshipsRetriever(AbstractCreateObjectFromSTIX):

    _KEYS_TO_DELETE: tuple = (
        'object_marking_refs',
        'x_mitre_modified_by_ref',
        'created_by_ref',
        'source_ref',
        'target_ref'
    )

    def __init__(self):
        super().__init__(MyRelationship, RelationshipSTIX)

    # get list of MyRelationship object
    def get_my_relationships(self, stix_object: dict) -> tuple:
        list_relationships = []
        for rel_obj in stix_object['relationships']:
            list_relationships.append(self._get_object_from_stix(rel_obj))
        return tuple(list_relationships)