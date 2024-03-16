from dataclasses import dataclass, field
from typing import List

from src.Domain.STIXObject.AbstractMySTIXObject import AbstractMySTIXObject
from src.Domain.STIXObject.MyExternalReference import MyExternalReference
from src.Domain.STIXObject.MyKillChainPhase import MyKillChainPhase


@dataclass
class MyAttackPattern(AbstractMySTIXObject):
    kill_chain_phases: tuple[MyKillChainPhase] = field(default_factory=tuple)
    x_mitre_data_sources: tuple[str] = field(default_factory=tuple)
    x_mitre_defense_bypassed: tuple[str] = field(default_factory=tuple)
    x_mitre_platforms: tuple[str] = field(default_factory=tuple)
    x_mitre_is_subtechnique: bool = False
    x_mitre_detection: str = ""
    x_mitre_permissions_required: tuple[str] = field(default_factory=tuple)
    x_mitre_remote_support: bool = False
    x_mitre_system_requirements: tuple[str] = field(default_factory=tuple)
    x_mitre_impact_type: tuple[str] = field(default_factory=tuple)
    x_mitre_effective_permissions: tuple[str] = field(default_factory=tuple)
    x_mitre_network_requirements: tuple[str] = field(default_factory=tuple)
    # x_mitre_modified_by_ref: str
    # object_marking_refs: List[str]
