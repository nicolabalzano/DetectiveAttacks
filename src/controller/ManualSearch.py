from src.model.container import AttackPatternsContainer, CampaignsContainer, ToolsMalwareContainer, AssetContainer, \
    MitreToCVEContainer


def get_searched_obj(searched_str: str):
    searched_list_obj = []

    # search in STIX
    searched_list_obj += __get_search_stix(searched_str)

    # search in CVE
    searched_list_obj += __get_searched_cve(searched_str)

    return searched_list_obj


def __get_searched_cve(searched_str: str):
    # Retrieve objects based on CVE ID
    objects = MitreToCVEContainer().get_objects_from_data_by_vuln_id(searched_str)

    # Create a dictionary with unique 'capability_id' as keys
    unique_objects = {obj['capability_id']: obj for obj in objects if obj['capability_id']}

    # Convert dictionary values to a list
    unique_list = list(unique_objects.values())

    # Format the objects and sort them
    formatted_list = sorted(
        [
            ['mapped vulnerability', obj['capability_id'], obj['capability_description'].strip(), 'CVE']
            for obj in unique_list if obj['capability_description']
        ],
        key=lambda obj: (obj[0], obj[2])
    )

    return formatted_list


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
        for obj in searched_set_obj if obj.x_mitre_id and obj.name
    ]

    searched_list_obj = sorted(searched_list_obj, key=lambda obj: (obj[0], obj[2]))

    return searched_list_obj