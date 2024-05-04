import numpy as np

from src.controller.objectsController.stixController.CampaignController import get_campaign_from_camp_rel_dict
from src.controller.objectsController.stixController.ToolMalwareController import get_tool_malware_from_tw_rel_dict
from src.controller.objectsController.util import format_list_of_string, format_external_references, \
    format_related_attack_patterns, remove_empty_values
from src.model.container import IntrusionSetsContainer


def get_intrusion_set_from_mitre_id(mitre_id: str):
    """
    Get intrusion_sets from mitre id

    :param mitre_id: str
    :return: list
    """
    ins = IntrusionSetsContainer().get_object_from_data_by_mitre_id(mitre_id)
    dict_ins = {}
    dict_ins['ID'] = ins.x_mitre_id
    dict_ins['Name'] = ins.name
    dict_ins['Type'] = ins.type
    dict_ins['Description'] = ins.description
    dict_ins['Domains'] = format_list_of_string(ins.x_mitre_domains)
    dict_ins['Aliases'] = format_list_of_string(ins.aliases)
    dict_ins['x_mitre_version'] = ins.x_mitre_version
    dict_ins['External references'] = format_external_references(ins.external_references)
    dict_ins['Revoked'] = ins.revoked
    dict_ins['Related Attack Patterns'] = format_related_attack_patterns(ins.attack_patterns_and_relationship)
    dict_ins['Tools and Malware used by group'] = get_tool_malware_from_tw_rel_dict(ins.tool_malware_and_relationship)
    dict_ins['Campaigns attributed to group'] = get_campaign_from_camp_rel_dict(ins.campaigns_and_relationship)

    return remove_empty_values(dict_ins)


def get_intrusion_set_probability_from_attack_patterns(attack_pattern_id_list):
    """
    Get the intrusion set probability from the attack pattern id
    :param attack_pattern_id_list: the list of attack pattern id
    :return: the dict of groups_probability
    """
    dict_ins_count = __get_intrusion_set_from_attack_pattern(attack_pattern_id_list)

    dict_ins_probability = __get_softmax_intrusion_set(dict_ins_count)

    return dict_ins_probability


def __get_softmax_intrusion_set(intrusion_set_num_of_attack_patterns):
    """
    Get the softmax of the intrusion set prediction
    :param intrusion_set_num_of_attack_patterns: dict[intrusion_set, num_of_attack_patterns]
    :return:
    """

    scores = np.array(list(intrusion_set_num_of_attack_patterns.values()))
    e_x = np.exp(scores - np.max(scores))
    softmax_scores = e_x / e_x.sum(axis=0)

    return dict(zip(intrusion_set_num_of_attack_patterns.keys(), softmax_scores))


def __get_intrusion_set_from_attack_pattern(attack_pattern_id_list):
    """
    Get the intrusion set from the attack pattern id
    :param attack_pattern_id_list: the list of attack pattern id
    :return: the list of groups
    """
    dict_ins_count = {}
    for at in attack_pattern_id_list:
        ins_list = IntrusionSetsContainer().get_objects_related_by_attack_pattern_id(at)
        for ins in ins_list:
            if ins in dict_ins_count:
                dict_ins_count[ins] += 1
            else:
                dict_ins_count[ins] = 1

    return dict_ins_count
