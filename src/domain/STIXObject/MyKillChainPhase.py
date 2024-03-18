from dataclasses import dataclass


@dataclass(eq=False, frozen=True)
class MyKillChainPhase:
    kill_chain_name: str
    phase_name: str

    def __eq__(self, other) -> bool:
        if not isinstance(other, MyKillChainPhase):
            return False
        return self.phase_name == other.phase_name

    def __hash__(self) -> int:
        return hash(self.phase_name)