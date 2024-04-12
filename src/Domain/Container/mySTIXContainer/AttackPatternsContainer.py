from stix2.v20 import KillChainPhase, Relationship

from src.domain.business.AttackPhase import AttackPhase
from src.domain.business.mySTIXObject import MyAttackPattern
from src.domain.container.mySTIXContainer.AbstractContainerMyStix import AbstractContainerMyStix
from src.domain.Singleton import singleton
from src.domain.container.mySTIXContainer.AssetContainer import AssetContainer
from src.domain.container.mySTIXContainer.CampaignsContainer import CampaignsContainer
from src.domain.container.mySTIXContainer.ToolsMalwareContainer import ToolsMalwareContainer


@singleton
class AttackPatternsContainer(AbstractContainerMyStix):

    # get related attack patterns from an attack pattern
    def get_related_attack_patterns_by_attack_pattern_id(self, attack_pattern_id: str) -> dict:
        related_attack_patterns = {}

        from_campaigns = CampaignsContainer().get_related_attack_patterns_by_attack_pattern_id(attack_pattern_id)
        related_attack_patterns.update(from_campaigns)

        from_toolsmalware = ToolsMalwareContainer().get_related_attack_patterns_by_attack_pattern_id(attack_pattern_id)
        related_attack_patterns.update(from_toolsmalware)

        from_assets = AssetContainer().get_related_attack_patterns_by_attack_pattern_id(attack_pattern_id)
        related_attack_patterns.update(from_assets)

        return related_attack_patterns

    def get_probably_happened_attack_patterns_grouped_by_phase(self, attacks_pattern: MyAttackPattern) -> dict:
        return self.__get_probably_happened_or_futured_attack_patterns_grouped_by_phase(attacks_pattern, False)

    def get_futured_attack_patterns_grouped_by_phase(self, attacks_pattern: MyAttackPattern) -> dict:
        return self.__get_probably_happened_or_futured_attack_patterns_grouped_by_phase(attacks_pattern, True)

    def __get_probably_happened_or_futured_attack_patterns_grouped_by_phase(self, attack_pattern: MyAttackPattern,
                                                                            future_or_happened: bool) -> dict:
        dict_kill_chain_phases = {}
        ats_rel = self.get_related_attack_patterns_by_attack_pattern_id(attack_pattern.id)
        # for related attack pattern
        for at, rel in ats_rel.items():
            # for kill chain phase of related attack pattern
            for atp1 in at.kill_chain_phases:
                # for kill chain phase of input attack_pattern
                for atp2 in attack_pattern.kill_chain_phases:
                    # TRUE -> futured  FALSE -> probably happened
                    if future_or_happened:
                        # if one phase is after of another add related attack pattern to the returned set
                        if AttackPhase.get_phase_value_from_name(
                                atp1.phase_name) > AttackPhase.get_phase_value_from_name(atp2.phase_name):
                            dict_kill_chain_phases = self.__update_dict_grouped_by_kcp(atp1, dict_kill_chain_phases, at,
                                                                                       rel)
                    else:
                        # if one phase is before of another add related attack pattern to the returned set
                        if AttackPhase.get_phase_value_from_name(
                                atp1.phase_name) <= AttackPhase.get_phase_value_from_name(atp2.phase_name):
                            dict_kill_chain_phases = self.__update_dict_grouped_by_kcp(atp1, dict_kill_chain_phases, at,
                                                                                       rel)

        return dict_kill_chain_phases

    """
    This method create and update the dict[MyAttackPattern, [Relationship] to return futured and happened attack pattern
    """

    def __update_dict_grouped_by_kcp(self, atp: KillChainPhase, dict_kill_chain_phases: dict, at: MyAttackPattern,
                                     rel: Relationship) -> dict:
        # if kill chain phase is not in dictionary, add it
        at_rel = {at: rel}
        if atp.phase_name not in dict_kill_chain_phases:
            dict_kill_chain_phases[atp.phase_name] = at_rel
        # if kill chain phase is in dictionary, update the dict
        else:
            dict_kill_chain_phases[atp.phase_name].update(at_rel)

        return dict_kill_chain_phases
