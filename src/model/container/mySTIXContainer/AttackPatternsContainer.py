from stix2.v20 import KillChainPhase, Relationship

from src.model.domain.AttackPhase import AttackPhase
from src.model.domain.mySTIXObject import MyAttackPattern
from src.model.container.mySTIXContainer.AbstractContainerMyStix import AbstractContainerMyStix
from src.model.Singleton import singleton
from src.model.container.mySTIXContainer.AssetContainer import AssetContainer
from src.model.container.mySTIXContainer.CampaignsContainer import CampaignsContainer
from src.model.container.mySTIXContainer.ToolsMalwareContainer import ToolsMalwareContainer


@singleton
class AttackPatternsContainer(AbstractContainerMyStix):

    def get_all_platforms(self) -> list:
        platforms = set()
        for attack_pattern in self.get_tuple_data():
            for platform in attack_pattern.x_mitre_platforms:
                platforms.add(platform)
        return list(platforms)

    # get related attack patterns from an attack pattern
    def get_related_attack_patterns_by_attack_pattern_id(self, attack_pattern_id: str) -> dict:
        related_attack_patterns = {}

        # get related attack patterns from campaigns, tools and malware, and assets
        # (no groups, because groups contains campaigns, tools and malware like a russian doll)
        from_campaigns = CampaignsContainer().get_related_attack_patterns_by_attack_pattern_id(attack_pattern_id)
        related_attack_patterns.update(from_campaigns)

        from_toolsmalware = ToolsMalwareContainer().get_related_attack_patterns_by_attack_pattern_id(attack_pattern_id)
        related_attack_patterns.update(from_toolsmalware)

        from_assets = AssetContainer().get_related_attack_patterns_by_attack_pattern_id(attack_pattern_id)
        related_attack_patterns.update(from_assets)

        return related_attack_patterns

    def get_all_related_attack_patterns_grouped_by_CKCPhase(self, attacks_pattern: MyAttackPattern) -> dict:
        phase__at_rel = self.get_all_related_attack_patterns_grouped_by_phase(attacks_pattern)
        return self.__group_by_CKC_phases_from_Mitre_phases(phase__at_rel)

    def get_probably_happened_attack_patterns_grouped_by_CKCPhase(self, attacks_pattern: MyAttackPattern) -> dict:
        phase__at_rel = self.get_probably_happened_attack_patterns_grouped_by_phase(attacks_pattern)
        return self.__group_by_CKC_phases_from_Mitre_phases(phase__at_rel)

    def get_futured_attack_patterns_grouped_by_CKCPhase(self, attacks_pattern: MyAttackPattern) -> dict:
        phase__at_rel = self.get_futured_attack_patterns_grouped_by_phase(attacks_pattern)
        return self.__group_by_CKC_phases_from_Mitre_phases(phase__at_rel)

    @classmethod
    def __group_by_CKC_phases_from_Mitre_phases(cls, phase__at_rel):
        """
        Group attack patterns by CKC phase
        :param phase__at_rel: dict of {phase: {attack_pattern: relationship}}
        :return: dict of {CKC_phase: {attack_pattern: relationship}}
        """
        ckc_phase__at_rel = {}

        # generate the dictionary with all the CKC phases
        for kckp in AttackPhase.get_CKC_mapping_to_phases().keys():
            ckc_phase__at_rel[kckp] = {}

        for phase, at_rel in phase__at_rel.items():
            for at, rel in at_rel.items():
                ckc_phase = AttackPhase.get_CKC_phase_from_phase(AttackPhase.get_enum_from_string(phase))
                if at not in ckc_phase__at_rel[ckc_phase]:
                    ckc_phase__at_rel[ckc_phase][at] = rel

        return ckc_phase__at_rel

    def get_attack_patterns_grouped_by_CKCPhase(self) -> dict:
        """
        Get attack patterns grouped by CKC phase
        :return: dict of {CKC_phase: [attack_pattern]}
        """
        attack_patterns = self.get_tuple_data()
        ckc_phase__ats = {}

        # generate the dictionary with all the CKC phases
        for kckp in AttackPhase.get_CKC_mapping_to_phases().keys():
            ckc_phase__ats[kckp] = []

        # group attack patterns by CKC phase
        for at in attack_patterns:
            # for each phase of the attack pattern
            for phase in at.kill_chain_phases:
                ckc_phase = AttackPhase.get_CKC_phase_from_phase(AttackPhase.get_enum_from_string(phase.phase_name))
                # if the attack pattern is not in the list of the CKC phase, add it (to not have duplicates)
                if at not in ckc_phase__ats[ckc_phase]:
                    ckc_phase__ats[ckc_phase].append(at)

        return ckc_phase__ats

    def get_all_related_attack_patterns_grouped_by_phase(self, attacks_pattern: MyAttackPattern) -> dict:
        return self.__get_probably_happened_or_futured_or_all_attack_patterns_grouped_by_phase(attacks_pattern, 0)

    def get_probably_happened_attack_patterns_grouped_by_phase(self, attacks_pattern: MyAttackPattern) -> dict:
        return self.__get_probably_happened_or_futured_or_all_attack_patterns_grouped_by_phase(attacks_pattern, 2)

    def get_futured_attack_patterns_grouped_by_phase(self, attacks_pattern: MyAttackPattern) -> dict:
        return self.__get_probably_happened_or_futured_or_all_attack_patterns_grouped_by_phase(attacks_pattern, 1)

    def __get_probably_happened_or_futured_or_all_attack_patterns_grouped_by_phase(self,
                                                                                   attack_pattern: MyAttackPattern,
                                                                                   future_or_happened_or_all: int) -> dict:
        dict_kill_chain_phases = {}
        ats_rel = self.get_related_attack_patterns_by_attack_pattern_id(attack_pattern.id)
        # for related attack pattern
        for at, rel in ats_rel.items():
            # for kill chain phase of related attack pattern
            for atp1 in at.kill_chain_phases:
                # for kill chain phase of input attack_pattern
                for atp2 in attack_pattern.kill_chain_phases:

                    # 0 -> All  1 -> futured  2 -> happened
                    if future_or_happened_or_all == 0:
                        dict_kill_chain_phases = self.__update_dict_grouped_by_kcp(atp1, dict_kill_chain_phases, at,
                                                                                   rel)
                    elif future_or_happened_or_all == 1:
                        # if one phase is after of another add related attack pattern to the returned set
                        if AttackPhase.get_phase_value_from_name(
                                atp1.phase_name) > AttackPhase.get_phase_value_from_name(atp2.phase_name):
                            dict_kill_chain_phases = self.__update_dict_grouped_by_kcp(atp1, dict_kill_chain_phases, at,
                                                                                       rel)
                    elif future_or_happened_or_all == 2:
                        # if one phase is before of another add related attack pattern to the returned set
                        if AttackPhase.get_phase_value_from_name(
                                atp1.phase_name) <= AttackPhase.get_phase_value_from_name(atp2.phase_name):
                            dict_kill_chain_phases = self.__update_dict_grouped_by_kcp(atp1, dict_kill_chain_phases, at,
                                                                                       rel)

        # Remove the searched attack pattern from the dictionary
        for phase in list(dict_kill_chain_phases.keys()):
            if attack_pattern in dict_kill_chain_phases[phase]:
                del dict_kill_chain_phases[phase][attack_pattern]
                if not dict_kill_chain_phases[phase]:
                    del dict_kill_chain_phases[phase]

        return dict_kill_chain_phases

    def __update_dict_grouped_by_kcp(self, atp: KillChainPhase, dict_kill_chain_phases: dict, at: MyAttackPattern,
                                     rel: Relationship) -> dict:
        """
            This method create and update the dict[MyAttackPattern, [Relationship] to return futured and happened attack pattern
            """
        # if kill chain phase is not in dictionary, add it
        at_rel = {at: rel}
        if atp.phase_name not in dict_kill_chain_phases:
            dict_kill_chain_phases[atp.phase_name] = at_rel
        # if kill chain phase is in dictionary, update the dict
        else:
            dict_kill_chain_phases[atp.phase_name].update(at_rel)

        return dict_kill_chain_phases
