from stix2.v20 import AttackPattern

from src.Domain.Conversion.AbstractObjectRetriever import AbstractObjectRetriever
from src.Domain.MitreAttackData.MitreAttackData import mitre_attack_data
from src.Domain.STIXObject.MyAttackPattern import MyAttackPattern
from src.Domain.Singleton import singleton


@singleton
class AttackPatternsRetriever(AbstractObjectRetriever):

    _KEYS_TO_DELETE: tuple = (
        'object_marking_refs',
        'x_mitre_modified_by_ref',
        'created_by_ref'
    )

    def __init__(self):
        super().__init__(MyAttackPattern, AttackPattern)

    def _get_all(self):
        return mitre_attack_data.get_techniques(remove_revoked_deprecated=True)
