from flask import send_file

from src.model.domain.AttackPhase import AttackPhase


def format_mitre_kill_chain_phases(kill_chain_phases):
    formatted_string = [__format_kill_chain_phase(phase.phase_name) + ' (' + phase.kill_chain_name + ')' for phase in
                        kill_chain_phases]
    return ', '.join(formatted_string)


def format_kill_chain_phases(obj):
    ckc_phases = []
    for kcp in obj.kill_chain_phases:
        ckc_phase = __format_kill_chain_phase(
            AttackPhase.get_CKC_phase_from_phase(AttackPhase.get_enum_from_string(kcp.phase_name)).title())
        if ckc_phase not in ckc_phases:
            ckc_phases.append(ckc_phase)
    return ckc_phases


def __format_kill_chain_phase(kill_chain_phase: str) -> str:
    new_str = kill_chain_phase.replace('-', ' ').title()
    new_str = new_str.replace('_', ' ').title()

    return new_str


def format_list_of_string(list_of_string):
    if not isinstance(list_of_string, list):
        return list_of_string
    return ', '.join(list_of_string)


def format_external_references(external_references: list) -> list[dict]:
    formatted_references = []
    for er in external_references:
        try:
            formatted_references.append({
                'Source Name': er.source_name,
                'URL': er.url
            })
        except AttributeError:
            pass
    return formatted_references


def format_related_attack_patterns(related_attack_patterns_rel: dict) -> list[dict]:
    if related_attack_patterns_rel:
        formatted_attack_patterns_by_phases = {}
        formatted_attack_patterns_by_phases_list = []

        for attack_pattern, rel in related_attack_patterns_rel.items():

            # Grouping the information in a dictionary by Cyber Kill Chain Phase
            KillChainPhases = format_kill_chain_phases(attack_pattern)
            for phase in KillChainPhases:
                if phase not in formatted_attack_patterns_by_phases:
                    formatted_attack_patterns_by_phases[phase] = []

                dict_ = {}
                dict_['ID'] = attack_pattern.x_mitre_id
                dict_['Name'] = attack_pattern.name
                dict_['Type'] = attack_pattern.type
                dict_['Description'] = attack_pattern.description
                dict_['Purpose'] = format_list_of_string(rel.relationship_type)
                dict_['Suggestion for this case'] = format_list_of_string(rel.description)
                dict_['Kill Chain phases'] = format_list_of_string(KillChainPhases)
                dict_['Mitre Kill Chain phases'] = format_mitre_kill_chain_phases(attack_pattern.kill_chain_phases)
                dict_['Platforms'] = format_list_of_string(attack_pattern.x_mitre_platforms)
                dict_ = remove_empty_values(dict_)

                formatted_attack_patterns_by_phases[phase].append(dict_)

        # because React can't render a dictionary, we need to convert it to a list
        for phase, attack_patterns in formatted_attack_patterns_by_phases.items():
            formatted_attack_patterns_by_phases_list.append({
                phase: attack_patterns
            })
        return formatted_attack_patterns_by_phases_list

    return []


def check_if_all_values_in_dict_list_are_empty(dict_list):
    """
    Check if all values in a list of dictionaries are empty
    :param dict_list: List of dictionaries
    :return: True if all values are empty, False otherwise
    """
    for dict_ in dict_list:
        for value in dict_.values():
            if value is not None and value != '' and value != []:
                return dict_list
    return None


def remove_empty_values(dict_):
    """
    Recursive function to remove key for empty string values
    :param dict_: dict
    :return: dict with empty values removed
    """
    for key in list(dict_.keys()):  # Use list to create a copy of the dictionary's keys
        value = dict_[key]
        if isinstance(value, dict):
            remove_empty_values(value)
            if not value:  # If the nested dictionary is now empty, remove it
                del dict_[key]
        elif isinstance(value, list):
            new_list = [item for item in value if item]  # Create a new list excluding empty items
            if new_list:  # If the new list is not empty, update the value in the dictionary
                dict_[key] = new_list
            else:  # If the new list is empty, remove the key from the dictionary
                del dict_[key]
        elif not value:  # If the value is an empty string or None, remove the key from the dictionary
            del dict_[key]
    return dict_


def download_file(file_path):
    return send_file(file_path, as_attachment=True, download_name=file_path.split('/')[-1])


