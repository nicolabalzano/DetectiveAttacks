from enum import Enum


class AttackPhase(Enum):
    RECONNAISSANCE = 1
    RESOURCE_DEVELOPMENT = 2
    INITIAL_ACCESS = 3
    ML_MODEL_ACCESS = 4
    EXECUTION = 5
    PERSISTENCE = 6
    PRIVILEGE_ESCALATION = 7
    DEFENSE_EVASION = 8
    EVASION = 8
    CREDENTIAL_ACCESS = 9
    DISCOVERY = 10
    LATERAL_MOVEMENT = 11
    COMMAND_AND_CONTROL = 12
    COLLECTION = 13
    INHIBIT_RESPONSE_FUNCTION = 14
    ML_ATTACK_STAGING = 15
    IMPAIR_PROCESS_CONTROL = 16
    EXFILTRATION = 17
    IMPACT = 18

    def get_phase_name(self):
        return self.name.lower().replace('_', '-')

    @classmethod
    def get_enum_from_string(cls, name):
        formatted_name = name.upper().replace(' ', '_')
        formatted_name = formatted_name.upper().replace('-', '_')
        phase = getattr(cls, formatted_name, None)
        if phase:
            return phase.value
        else:
            # Verifica se formatted_name è un alias
            if formatted_name in cls.__members__:
                return cls.__members__[formatted_name]
        return None

    @classmethod
    def get_phase_value_from_name(cls, name):
        formatted_name = name.upper().replace(' ', '_')
        formatted_name = formatted_name.upper().replace('-', '_')
        phase = getattr(cls, formatted_name, None)
        if phase:
            return phase.value
        else:
            # Verifica se formatted_name è un alias
            if formatted_name in cls.__members__:
                return cls.__members__[formatted_name].value
            return None