from dataclasses import dataclass

from src.domain.MySTIXObject.AttackPhase import AttackPhase


@dataclass(eq=False, frozen=True)
class MyKillChainPhase:
    kill_chain_name: str
    phase_name: AttackPhase

    def __init__(self, kill_chain_name: str, phase_name: str):
        enum_phase_name = AttackPhase.get_enum_from_string(phase_name)
        if enum_phase_name is None:
            raise ValueError(f"No enum member found for phase name: {phase_name}")

        object.__setattr__(self, 'kill_chain_name', kill_chain_name)
        object.__setattr__(self, 'phase_name', enum_phase_name)

    def __eq__(self, other) -> bool:
        if not isinstance(other, MyKillChainPhase):
            return False
        return self.phase_name == other.phase_name

    def __hash__(self) -> int:
        return hash(self.phase_name)

