from enum import Enum


class AttackPhase(Enum):
    RECONNAISSANCE = 1
    RESOURCE_DEVELOPMENT = 2
    INITIAL_ACCESS = 3
    EXECUTION = 4
    PERSISTENCE = 5
    PRIVILEGE_ESCALATION = 6
    DEFENSE_EVASION = 7
    CREDENTIAL_ACCESS = 8
    DISCOVERY = 9
    LATERAL_MOVEMENT = 10
    COLLECTION = 11
    COMMAND_AND_CONTROL = 12
    EXFILTRATION = 13
    IMPACT = 14

    def get_phase_name(self):
        return self.name.lower().replace('_', '-')

    @classmethod
    def get_phase_value_from_name(cls, name):
        formatted_name = name.upper().replace('-', '_')
        for phase in cls:
            if phase.name == formatted_name:
                return phase.value
        # Ritorna None o solleva un'eccezione se il nome non è trovato
        return None