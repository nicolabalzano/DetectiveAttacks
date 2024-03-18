from dataclasses import dataclass, field
from typing import Tuple, Dict

from src.Domain.STIXObject.AbstractMySTIXObjectWithContributors import AbstractMySTIXObjectWithContributors
from src.Domain.STIXObject.MyCourseOfAction import MyCourseOfAction
from src.Domain.STIXObject.MyKillChainPhase import MyKillChainPhase
from src.Domain.STIXObject.MyRelationship import MyRelationship
from src.Domain.STIXObject.convert_lists_to_tuples_in_init import convert_lists_to_tuples_in_init


@convert_lists_to_tuples_in_init
@dataclass(eq=False, frozen=True)
class MyAttackPattern(AbstractMySTIXObjectWithContributors):
    kill_chain_phases: Tuple[MyKillChainPhase] = field(default_factory=tuple)
    x_mitre_data_sources: Tuple[str] = field(default_factory=tuple)
    x_mitre_defense_bypassed: Tuple[str] = field(default_factory=tuple)
    x_mitre_platforms: Tuple[str] = field(default_factory=tuple)
    x_mitre_is_subtechnique: bool = False
    x_mitre_detection: str = ""
    x_mitre_permissions_required: Tuple[str] = field(default_factory=tuple)
    x_mitre_remote_support: bool = False
    x_mitre_system_requirements: Tuple[str] = field(default_factory=tuple)
    x_mitre_impact_type: Tuple[str] = field(default_factory=tuple)
    x_mitre_effective_permissions: Tuple[str] = field(default_factory=tuple)
    x_mitre_network_requirements: Tuple[str] = field(default_factory=tuple)
    courses_of_action_and_relationship: Tuple[Dict[MyCourseOfAction, tuple[MyRelationship]]] = field(default_factory=tuple)
    # x_mitre_modified_by_ref: str
    # object_marking_refs: List[str]

    def __eq__(self, other) -> bool:
        if not isinstance(other, MyAttackPattern):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)