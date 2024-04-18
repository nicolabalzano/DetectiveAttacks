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
    dict_at['Impact type'] = __format_list_of_string(at.x_mitre_impact_type)
    dict_at['Platforms'] = __format_list_of_string(at.x_mitre_platforms)
    dict_at['Detection'] = at.x_mitre_detection
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
    dict_at['Data Source'] = __format_list_of_string(at.x_mitre_data_sources)
    dict_at['Defense Bypassed'] = __format_list_of_string(at.x_mitre_defense_bypassed)
    dict_at['Mitre version'] = at.x_mitre_version
    dict_at['Deprecated'] = at.x_mitre_deprecated
    dict_at['Revoked'] = at.revoked
    dict_at['Is a sub-technique'] = at.x_mitre_is_subtechnique
    dict_at['Remote support'] = at.x_mitre_remote_support
    dict_at['Tactic type'] = at.x_mitre_tactic_type
    dict_at['External references'] = [
        {
            'Source Name': er.source_name,
            'URL': er.url
        } for er in at.external_references
    ]

    return dict_at


def __format_kill_chain_phases(kill_chain_phases):
    formatted_string = ""
    for phase in kill_chain_phases:
        formatted_string += "{1} ({0}), ".format(phase.kill_chain_name, phase.phase_name)
    return formatted_string.rstrip(', ')

def __format_list_of_string(list_of_string):
    return ', '.join(list_of_string)
