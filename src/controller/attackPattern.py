from src.model.container import AttackPatternsContainer


def get_attack_patter_from_mitre_id(mitre_id: str):
    """
    Get the attack pattern object from the mitre id
    :param mitre_id: the mitre id
    :return: the MyAttackPattern object
    """

    dict_at = {}
    at = AttackPatternsContainer().get_object_from_data_by_mitre_id(mitre_id)
    dict_at['ID'] = at.x_mitre_id
    dict_at['Name'] = at.name
    dict_at['Type'] = at.type
    dict_at['Description'] = at.description
    dict_at['Domains'] = __format_list_of_string(at.x_mitre_domains)
    dict_at['Kill Chain phases'] = __format_kill_chain_phases(at.kill_chain_phases)
    dict_at['Platforms'] = __format_list_of_string(at.x_mitre_platforms)
    dict_at['Detection suggestions'] = at.x_mitre_detection
    dict_at['Mitigations'] = [
        {
            'ID': coa.x_mitre_id,
            'Name': coa.name,
            'Description': coa.description,
            'Type': coa.type,
            'Type of relationship': rel.relationship_type,
            'Description of relationship': rel.description,
            'External references': [
                {
                    'Source Name': er.source_name,
                    'URL': er.url
                } for er in coa.external_references
            ]
        } for coa, rel in at.courses_of_action_and_relationship.items()
    ]
    dict_at['Permission requirements'] = __format_list_of_string(at.x_mitre_permissions_required)
    dict_at['Effective permissions'] = __format_list_of_string(at.x_mitre_effective_permissions)
    dict_at['System requirements'] = __format_list_of_string(at.x_mitre_system_requirements)
    dict_at['Network requirements'] = __format_list_of_string(at.x_mitre_network_requirements)
    dict_at['Impact type'] = __format_list_of_string(at.x_mitre_impact_type)
    dict_at['Data Source'] = __format_list_of_string(at.x_mitre_data_sources)
    dict_at['Defense Bypassed'] = __format_list_of_string(at.x_mitre_defense_bypassed)
    dict_at['Mitre version'] = __format_list_of_string(at.x_mitre_version)
    dict_at['Deprecated'] = __format_list_of_string(at.x_mitre_deprecated)
    dict_at['Revoked'] = __format_list_of_string(at.revoked)
    dict_at['Is a sub-technique'] = at.x_mitre_is_subtechnique
    dict_at['Remote support'] = __format_list_of_string(at.x_mitre_remote_support)
    dict_at['Tactic type'] = __format_list_of_string(at.x_mitre_tactic_type)
    dict_at['External references'] = [
        {
            'Source Name': er.source_name,
            'URL': er.url
        } for er in at.external_references
    ]

    return remove_empty_values(dict_at)


def __format_kill_chain_phases(kill_chain_phases):
    formatted_string = ""
    for phase in kill_chain_phases:
        formatted_string += "{1} ({0}), ".format(phase.kill_chain_name, phase.phase_name)
    return formatted_string.rstrip('.\n')


def __format_list_of_string(list_of_string):
    if not isinstance(list_of_string, list):
        return list_of_string
    return ', '.join(list_of_string)


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
