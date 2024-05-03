from src.controller.objectRender.util import format_list_of_string, format_external_references, \
    format_related_attack_patterns, remove_empty_values
from src.model.container import AssetContainer


def get_asset_from_ass_rel_dict(dict_ass_rel):
    """
        Get asset from dict of {tool_malware: relationship}

        :param dict_ass_rel: {asset: relationship}
        :return: list
        """
    list_tw = []
    for asset, rel in dict_ass_rel.items():
        dict_a = {}
        dict_a['ID'] = asset.x_mitre_id
        dict_a['Name'] = asset.name
        dict_a['Type'] = asset.type
        dict_a['Description'] = asset.description
        dict_a['Purpose'] = format_list_of_string(rel.relationship_type)
        dict_a['Suggestion for this case'] = format_list_of_string(rel.description)
        dict_a['Domains'] = format_list_of_string(asset.x_mitre_domains)
        dict_a['Sectors'] = format_list_of_string(asset.x_mitre_sectors)
        dict_a['Platforms'] = format_list_of_string(asset.x_mitre_platforms)
        dict_a['External references'] = format_external_references(asset.external_references)
        dict_a = remove_empty_values(dict_a)
        list_tw.append(dict_a)
    return list_tw


def get_asset_from_mitre_id(mitre_id: str):
    """
    Get tool malware from mitre id

    :param mitre_id: str
    :return: list
    """
    asset = AssetContainer().get_object_from_data_by_mitre_id(mitre_id)
    dict_a = {}
    dict_a['ID'] = asset.x_mitre_id
    dict_a['Name'] = asset.name
    dict_a['Type'] = asset.type
    dict_a['Description'] = asset.description
    dict_a['Domains'] = format_list_of_string(asset.x_mitre_domains)
    dict_a['Platforms'] = format_list_of_string(asset.x_mitre_platforms)
    dict_a['x_mitre_version'] = asset.x_mitre_version
    dict_a['External references'] = format_external_references(asset.external_references)
    dict_a['Revoked'] = asset.revoked
    dict_a['Related Attack Patterns'] = format_related_attack_patterns(asset.attack_patterns_and_relationships)
    dict_a['Sectors'] = format_list_of_string(asset.x_mitre_sectors)
    dict_a['Related Assets'] = [{
        'Name': ass['name'],
        'Description': ass['description'],
        'Sectors': format_list_of_string(ass['related_asset_sectors'])
    }
        for ass in asset.x_mitre_related_assets]

    return remove_empty_values(dict_a)