from dataclasses import dataclass, field

from stix2.v20 import Relationship
from stix2.v20 import KillChainPhase

from src.domain.business.MySTIXObject.AbstractMySTIXObjectWithContributors import AbstractMySTIXObjectWithContributors
from src.domain.business.MySTIXObject.MyCourseOfAction import MyCourseOfAction


@dataclass(eq=False, frozen=True, slots=True)
class MyAttackPattern(AbstractMySTIXObjectWithContributors):
    kill_chain_phases: list[KillChainPhase] = field(default_factory=list)
    x_mitre_data_sources: list[str] = field(default_factory=list)
    x_mitre_defense_bypassed: list[str] = field(default_factory=list)
    x_mitre_platforms: list[str] = field(default_factory=list)
    x_mitre_is_subtechnique: bool = False
    x_mitre_detection: str = ""
    x_mitre_permissions_required: list[str] = field(default_factory=list)
    x_mitre_remote_support: bool = False
    x_mitre_system_requirements: list[str] = field(default_factory=list)
    x_mitre_impact_type: list[str] = field(default_factory=list)
    x_mitre_effective_permissions: list[str] = field(default_factory=list)
    x_mitre_network_requirements: list[str] = field(default_factory=list)
    courses_of_action_and_relationship: dict[MyCourseOfAction, list[Relationship]] = field(default_factory=dict)
    x_mitre_tactic_type: str = ""

    def __post_init__(self):
        for er in self.external_references:
            if '/techniques/' in er.url and 'mitre-' in er.source_name:
                object.__setattr__(self, 'x_mitre_id', f"{er.external_id}")
                break

    def __eq__(self, other) -> bool:
        if not isinstance(other, MyAttackPattern):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
