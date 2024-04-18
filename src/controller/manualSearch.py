from src.model.container import AttackPatternsContainer, CampaignsContainer, ToolsMalwareContainer, AssetContainer, \
    AttackToCVEContainer


def get_searched_obj(searched_str: str):
    searched_list_obj = []

    # search in STIX
    searched_list_obj += __get_search_stix(searched_str)

    # search in CVE
    searched_list_obj += __get_searched_cve(searched_str)

    return searched_list_obj


def __get_searched_cve(searched_str: str):
    searched_list_obj = AttackToCVEContainer().get_object_from_data_by_name(searched_str)
    found_obj = False

    for obj in AttackToCVEContainer().get_object_from_data_by_cve_id(searched_str):
        for obj_in_list in searched_list_obj:
            if obj['capability_id'] != obj_in_list['capability_id']:
                found_obj = True

        # if CVE is not in set
        if found_obj is False:
            searched_list_obj.append(obj)
        found_obj = False

    # RETURNED OBJECTS FORMAT: [type, x_mitre_id, name, x_mitre_domains]
    searched_list_obj = [['vulnerability', obj['capability_id'], obj['capability_description'], 'CVE'] for obj in searched_list_obj]

    searched_list_obj = sorted(searched_list_obj, key=lambda obj: (obj[0], obj[2]))

    return searched_list_obj


def __get_search_stix(searched_str: str):
    searched_set_obj = set()
    containers = [
        AttackPatternsContainer(),
        CampaignsContainer(),
        ToolsMalwareContainer(),
        AssetContainer(),
    ]

    for container in containers:
        objects = container.get_object_from_data_by_name(searched_str)
        for obj in objects:
            searched_set_obj.add(obj)

    # RETURNED OBJECTS FORMAT: [type, x_mitre_id, name, x_mitre_domains]
    searched_list_obj = [
        [
            obj.type,
            obj.x_mitre_id,
            obj.name,
            ', '.join([domain.split('-')[0] if '-' in domain else domain for domain in obj.x_mitre_domains]) or 'n/a'
        ]
        for obj in searched_set_obj
    ]

    searched_list_obj = sorted(searched_list_obj, key=lambda obj: (obj[0], obj[2]))

    return searched_list_obj
