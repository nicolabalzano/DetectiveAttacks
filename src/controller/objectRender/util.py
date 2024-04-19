from src.model.domain.AttackPhase import AttackPhase


def format_mitre_kill_chain_phases(kill_chain_phases):
    formatted_string = [__format_kill_chain_phase(phase.phase_name) + ' (' + phase.kill_chain_name + ')' for phase in
                        kill_chain_phases]
    return ', '.join(formatted_string)


def format_kill_chain_phases(obj):
    return [__format_kill_chain_phase(AttackPhase.get_enum_from_string(kcp.phase_name).get_phase_name())
            for kcp in obj.kill_chain_phases][0]


def __format_kill_chain_phase(kill_chain_phase: str):
    return kill_chain_phase.replace('-', ' ').title()


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


# recursive function to remove key for empty string values
def remove_empty_values(dictionary):
    for key in list(dictionary.keys()):  # Use list to create a copy of the dictionary's keys
        value = dictionary[key]
        if isinstance(value, dict):
            remove_empty_values(value)
            if not value:  # If the nested dictionary is now empty, remove it
                del dictionary[key]
        elif isinstance(value, list):
            new_list = [item for item in value if item]  # Create a new list excluding empty items
            if new_list:  # If the new list is not empty, update the value in the dictionary
                dictionary[key] = new_list
            else:  # If the new list is empty, remove the key from the dictionary
                del dictionary[key]
        elif not value:  # If the value is an empty string or None, remove the key from the dictionary
            del dictionary[key]
    return dictionary