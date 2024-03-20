from enum import Enum


class AttackPhase(Enum):
    RECONNAISSANCE = 1
    DISCOVERY = 2
    RESOURCE_DEVELOPMENT = 3
    CREDENTIAL_ACCESS = 4
    INITIAL_ACCESS = 5
    EXECUTION = 6
    DEFENSE_EVASION = 7
    PERSISTENCE = 8
    PRIVILEGE_ESCALATION = 9
    COMMAND_AND_CONTROL = 10
    LATERAL_MOVEMENT = 11
    COLLECTION = 12
    EXFILTRATION = 13
    IMPACT = 14

    def get_phase_name(self):
        return self.name.lower().replace('_', '-')

    @classmethod
    def get_enum_from_string(cls, name):
        formatted_name = name.upper().replace('-', '_')
        for phase in cls:
            if phase.name == formatted_name:
                return phase
        return None

    @classmethod
    def get_phase_value_from_name(cls, name):
        formatted_name = name.upper().replace('-', '_')
        for phase in cls:
            if phase.name == formatted_name:
                return phase.value
        return None