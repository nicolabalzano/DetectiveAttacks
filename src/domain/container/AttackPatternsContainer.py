from typing import Set

from stix2 import KillChainPhase

from src.domain.MySTIXObject.AttackPhase import AttackPhase
from src.domain.MySTIXObject.MyAttackPattern import MyAttackPattern
from src.domain.container.AbstractContainer import AbstractContainer
from src.domain.Singleton import singleton
from src.domain.container.CampaignsContainer import CampaignsContainer
from src.domain.container.ToolsMalwareContainer import ToolsMalwareContainer


@singleton
class AttackPatternsContainer(AbstractContainer):
    pass

    # get related attack patterns from an attack pattern
    def get_related_attack_patterns_by_attack_pattern(self, attack_pattern_id: str) -> Set:
        related_attack_patterns = set()

        campaigns = CampaignsContainer().get_related_attack_patterns_by_attack_pattern(attack_pattern_id)
        related_attack_patterns.update(campaigns)

        toolsmalware = ToolsMalwareContainer().get_related_attack_patterns_by_attack_pattern(attack_pattern_id)
        related_attack_patterns.update(toolsmalware)

        return related_attack_patterns

    def get_probably_happened_attack_patterns_grouped_by_phase(self, attack_pattern: MyAttackPattern) -> dict:
        return self.__get_probably_happened_or_futured_attack_patterns_grouped_by_phase(attack_pattern, False)

    def get_futured_attack_patterns_grouped_by_phase(self, attack_pattern: MyAttackPattern) -> dict:
        return self.__get_probably_happened_or_futured_attack_patterns_grouped_by_phase(attack_pattern, True)

    def __get_probably_happened_or_futured_attack_patterns_grouped_by_phase(self, attack_pattern: MyAttackPattern, future_or_happened: bool):
        dict_kill_chain_phases = {}

        # for related attack pattern
        for at in self.get_related_attack_patterns_by_attack_pattern(attack_pattern.id):
            # for kill chain phase of related attack pattern
            for atp1 in at.kill_chain_phases:
                # for kill chain phase of input attack_pattern
                for atp2 in attack_pattern.kill_chain_phases:

                    # TRUE -> futured  FALSE -> probably happened
                    if future_or_happened:
                        # if one phase is after of another add related attack pattern to the returned set
                        if AttackPhase.get_phase_value_from_name(atp1.phase_name) > AttackPhase.get_phase_value_from_name(atp2.phase_name):
                            dict_kill_chain_phases = self.__check_and_add_to_dict_by_kcp(atp1, dict_kill_chain_phases, at)
                    else:
                        # if one phase is before of another add related attack pattern to the returned set
                        if AttackPhase.get_phase_value_from_name(atp1.phase_name) <= AttackPhase.get_phase_value_from_name(atp2.phase_name):
                            dict_kill_chain_phases = self.__check_and_add_to_dict_by_kcp(atp1, dict_kill_chain_phases, at)

        return dict_kill_chain_phases

    def __check_and_add_to_dict_by_kcp(self, atp: KillChainPhase, dict_kill_chain_phases: dict, at: MyAttackPattern):
        # if kill chain phase is not in dictionary, add it
        if atp.phase_name not in dict_kill_chain_phases:
            dict_kill_chain_phases[atp.phase_name] = [at]
        # if kill chain phase is in dictionary, update the list
        else:
            dict_kill_chain_phases[atp.phase_name].append(at)

        return dict_kill_chain_phases
