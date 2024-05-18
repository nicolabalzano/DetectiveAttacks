from enum import Enum
from typing import Any


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
    NETWORK_EFFECTS = 18
    REMOTE_SERVICE_EFFECTS = 18


    @classmethod
    def get_CKC_mapping_to_phases(cls) -> dict:
        """
        Get the mapping of the phases to the Cyber Kill Chain
        :return: dict
        """
        return {
            'Reconnaissance': [1],
            'Weaponization': [2],
            'Delivery': [3, 4],
            'Exploitation': [5],
            'Installation': [6, 7, 8],
            'Command&Control': [9, 10, 11, 12, 13, 14],
            'Action on Objectives': [15, 16, 17, 18],
        }

    @classmethod
    def get_CKC_phase_from_phase(cls, kill_chain_phase: Enum) -> str:
        """
            This function is used to manage the mapping of phase to the Cyber Kill Chain
            :param kill_chain_phase: the phase of AttackPhase enum
            :return: the phase of the Cyber Kill Chain
        """

        for kc_phase, phases_value in cls.get_CKC_mapping_to_phases().items():
            if kill_chain_phase.value in phases_value:
                return kc_phase

    def get_phase_name(self):
        return self.name.lower().replace('_', ' ').title()

    @classmethod
    def __get_formatted_name_for_enum(cls, name: str) -> str:
        formatted_name = name.upper().replace(' ', '_')
        formatted_name = formatted_name.upper().replace('-', '_')
        return formatted_name

    @classmethod
    def get_enum_from_string(cls, name) -> Enum | None:
        """
        Get the phase enum from the name of the phase
        :param name:
        :return: enum of the phase or None if the phase doesn't exist
        """
        formatted_name = cls.__get_formatted_name_for_enum(name)
        phase = getattr(cls, formatted_name, None)
        if phase:
            return phase
        else:
            # Verifica se formatted_name è un alias
            if formatted_name in cls.__members__:
                return cls.__members__[formatted_name]
        return None

    @classmethod
    def get_phase_value_from_name(cls, name: str) -> int:
        """
        Get the value of the phase from the name of the phase
        :param name:
        :return: value of the phase in enum
        """
        formatted_name = cls.__get_formatted_name_for_enum(name)
        phase = getattr(cls, formatted_name, None)
        if phase:
            return phase.value
        else:
            # Verify if formatted_name is an alias
            if formatted_name in cls.__members__:
                return cls.__members__[formatted_name].value
            return None
