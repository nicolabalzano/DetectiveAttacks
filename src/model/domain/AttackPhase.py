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

    @classmethod
    def get_phase_from_CKC(cls, kill_chain_phase):
        CKC_phases = {
            'RECONNAISSANCE': [1],
            'WEAPONIZATION': [2],
            'DELIVERY': [3, 4],
            'EXPLOITATION': [5],
            'INSTALLATION': [6, 7, 8],
            'COMMAND_AND_CONTROL': [9, 10, 11, 12, 13, 14],
            'ACTIONS_ON_OBJECTIVES': [15, 16, 17, 18],
        }
        for kc_phase, phases_value in CKC_phases.items():
            if kill_chain_phase in phases_value:
                return kc_phase

    def get_phase_name(self):
        return self.name.lower().replace('_', '-')

    @classmethod
    def get_enum_from_string(cls, name):
        formatted_name = name.upper().replace(' ', '_')
        formatted_name = formatted_name.upper().replace('-', '_')
        phase = getattr(cls, formatted_name, None)
        if phase:
            return phase
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
