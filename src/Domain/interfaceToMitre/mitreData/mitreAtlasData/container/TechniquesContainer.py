from typing import List
from stix2.v20 import KillChainPhase
from stix2.v20 import AttackPattern

from src.domain.interfaceToMitre.mitreData.mitreAtlasData.container.AbstractAtlasContainer import AbstractAtlasContainer
from src.domain.Singleton import singleton
from src.domain.interfaceToMitre.mitreData.mitreAtlasData.utils.MitreAtlasUtils import get_uuid_from_string


@singleton
class TechniquesContainer(AbstractAtlasContainer):

    def __init__(self, dict_file: dict):
        self.dict_file = dict_file
        data = self.__define_all_techniques()
        super().__init__(data)

    def __define_all_techniques(self) -> List[AttackPattern]:
        list_attack_pattern = []
        tactics = []
        for at in (self.dict_file['matrices'][0])['techniques']:
            new_id = f"attack-pattern--{get_uuid_from_string(at['id'])}"
            if at["object-type"] == "technique":
                if 'tactics' in at.keys():
                    tactics = at['tactics']
                attack_pattern = AttackPattern(
                    id=new_id,
                    type='attack-pattern',
                    name=at['name'],
                    description=at['description'],
                    kill_chain_phases=[self.__get_tactic_by_id(tactic_id) for tactic_id in tactics],
                    external_references=super()._get_external_refs(at, 'techniques'),
                )
                list_attack_pattern.append(attack_pattern)
        return list_attack_pattern

    def __get_tactic_by_id(self, tactics_id: str) -> KillChainPhase | None:
        for tactic in self.dict_file['matrices'][0]['tactics']:
            if tactics_id == tactic['id']:
                kill_chain_phase = KillChainPhase(
                    kill_chain_name='atlas',
                    phase_name=tactic['name']
                )
                return kill_chain_phase
