from src.controller.objectRender.util import format_list_of_string, format_external_references, remove_empty_values, \
    format_related_attack_patterns
from src.model.container import CampaignsContainer


def get_campaign_from_camp_rel_dict(dict_camp_rel):
    """
    Get campaign from dict of {campaign: relationship}

    :param dict_camp_rel: [{tool_malware: relationship}]
    :return: list
    """
    list_camp = []
    for camp, rel in dict_camp_rel.items():
        dict_camp = {}
        dict_camp['ID'] = camp.x_mitre_id
        dict_camp['Name'] = camp.name
        dict_camp['Type'] = camp.type
        dict_camp['Description'] = camp.description
        dict_camp['Suggestion for this case'] = format_list_of_string(rel.description)
        dict_camp['Purpose'] = format_list_of_string(rel.relationship_type)
        dict_camp['Domains'] = format_list_of_string(camp.x_mitre_domains)
        dict_camp['Aliases'] = format_list_of_string(camp.aliases)
        dict_camp['Revoked'] = format_list_of_string(camp.revoked)
        dict_camp['External references'] = format_external_references(camp.external_references)
        dict_camp = remove_empty_values(dict_camp)
        list_camp.append(dict_camp)
    return list_camp


def get_campaign_from_mitre_id(mitre_id: str):
    """
    Get tool campaign from mitre id
    :param mitre_id:
    :return: list
    """

    camp = CampaignsContainer().get_object_from_data_by_mitre_id(mitre_id)
    dict_camp = {}
    dict_camp['ID'] = camp.x_mitre_id
    dict_camp['Name'] = camp.name
    dict_camp['Type'] = camp.type
    dict_camp['Description'] = camp.description
    dict_camp['Domains'] = format_list_of_string(camp.x_mitre_domains)
    dict_camp['Aliases'] = format_list_of_string(camp.aliases)
    dict_camp['x_mitre_version'] = camp.x_mitre_version
    dict_camp['External references'] = format_external_references(camp.external_references)
    dict_camp['Revoked'] = camp.revoked
    dict_camp['Related Attack Patterns'] = format_related_attack_patterns(camp.attack_patterns_and_relationships)

    return remove_empty_values(dict_camp)