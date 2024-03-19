from typing import Set

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

    def get_probably_happend_attack_patterns(self, attack_pattern: MyAttackPattern):
        probably_happened_attack_pattern = set()

        # for related attack pattern
        for at in self.get_related_attack_patterns_by_attack_pattern(attack_pattern.id):
            # for kill chain phase of related attack pattern
            for atp1 in at.kill_chain_phases:
                # for kill chain phase of input attack_pattern
                for atp2 in attack_pattern.kill_chain_phases:
                    # if one phase is before of another add related attack pattern to the returned set
                    if AttackPhase.get_phase_value_from_name(atp1.phase_name) <= AttackPhase.get_phase_value_from_name(atp2.phase_name):
                        probably_happened_attack_pattern.add(at)

        return probably_happened_attack_pattern

    def get_probably_futured_attack_patterns(self, attack_pattern: MyAttackPattern):
        probably_happened_attack_pattern = set()

        # for related attack pattern
        for at in self.get_related_attack_patterns_by_attack_pattern(attack_pattern.id):
            # for kill chain phase of related attack pattern
            for atp1 in at.kill_chain_phases:
                # for kill chain phase of input attack_pattern
                for atp2 in attack_pattern.kill_chain_phases:
                    # if one phase is after of another add related attack pattern to the returned set
                    if AttackPhase.get_phase_value_from_name(atp1.phase_name) > AttackPhase.get_phase_value_from_name(atp2.phase_name):
                        probably_happened_attack_pattern.add(at)

        return probably_happened_attack_pattern