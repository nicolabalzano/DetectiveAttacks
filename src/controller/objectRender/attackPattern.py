from src.controller.objectRender.toolMalware import get_tool_malware_from_tw_rel_dict
from src.controller.objectRender.util import format_list_of_string, remove_empty_values, format_kill_chain_phases, \
    format_mitre_kill_chain_phases, format_external_references
from src.model.container import AttackPatternsContainer, ToolsMalwareContainer, CampaignsContainer, AssetContainer


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
    dict_at['Domains'] = format_list_of_string(at.x_mitre_domains)
    dict_at['Kill Chain phases'] = format_kill_chain_phases(at)
    dict_at['Mitre Kill Chain phases'] = format_mitre_kill_chain_phases(at.kill_chain_phases)
    dict_at['Platforms'] = format_list_of_string(at.x_mitre_platforms)
    dict_at['Detection suggestions'] = at.x_mitre_detection
    dict_at['Mitigations'] = [
        {
            'ID': coa.x_mitre_id,
            'Name': coa.name,
            'Description': coa.description,
            'Type': coa.type,
            'Purpose': rel.relationship_type,
            'Suggestion for this case': rel.description,
            'External references': format_external_references(coa.external_references),
        } for coa, rel in at.courses_of_action_and_relationship.items()
    ]
    dict_at['Procedure examples'] = get_tool_malware_from_tw_rel_dict(
        ToolsMalwareContainer().get_object_using_attack_pattern_by_attack_pattern_id(at.id))
    dict_at['Permission requirements'] = format_list_of_string(at.x_mitre_permissions_required)
    dict_at['Effective permissions'] = format_list_of_string(at.x_mitre_effective_permissions)
    dict_at['System requirements'] = format_list_of_string(at.x_mitre_system_requirements)
    dict_at['Network requirements'] = format_list_of_string(at.x_mitre_network_requirements)
    dict_at['Impact type'] = format_list_of_string(at.x_mitre_impact_type)
    dict_at['Data Source'] = format_list_of_string(at.x_mitre_data_sources)
    dict_at['Defense Bypassed'] = format_list_of_string(at.x_mitre_defense_bypassed)
    dict_at['Mitre version'] = format_list_of_string(at.x_mitre_version)
    dict_at['Deprecated'] = format_list_of_string(at.x_mitre_deprecated)
    dict_at['Revoked'] = format_list_of_string(at.revoked)
    dict_at['Is a sub-technique'] = at.x_mitre_is_subtechnique
    dict_at['Remote support'] = format_list_of_string(at.x_mitre_remote_support)
    dict_at['Tactic type'] = format_list_of_string(at.x_mitre_tactic_type)
    dict_at['External references'] = format_external_references(at.external_references)
    dict_at['Attacks patterns that can lead to this'] = __get_related_attacks(AttackPatternsContainer().get_probably_happened_attack_patterns_grouped_by_phase, at)
    dict_at['Attacks patterns that may occur after this'] = __get_related_attacks(AttackPatternsContainer().get_futured_attack_patterns_grouped_by_phase, at)

    return (dict_at)


def __get_related_attacks(function_futured_or_past, attack_pattern):
    return [
        {
            phase: [
                {
                    'Name': '\"' + future_at.name + '\"' + ' from ' + __get_source_relationships(rel.source_ref).type + ' \"' + __get_source_relationships(rel.source_ref).name + '\"' ,
                    'Description': rel.description,
                    'ID': future_at.x_mitre_id,
                    'Relationship Source ID': __get_source_relationships(rel.source_ref).x_mitre_id,
                }
                for future_at, rel in future_ats.items()
            ]
        }
        for phase, future_ats in function_futured_or_past(attack_pattern).items()
    ]


def __get_source_relationships(source_id: str):
    containers = [
        AttackPatternsContainer(),
        CampaignsContainer(),
        ToolsMalwareContainer(),
        AssetContainer(),
    ]

    for container in containers:
        obj = container.get_object_from_data_by_id(source_id)
        if obj:
            return obj
    return None
