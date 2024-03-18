from dataclasses import dataclass


@dataclass(eq=False, frozen=True)
class MyKillChainPhase:
    kill_chain_name: str
    phase_name: str