import os.path
from datetime import datetime

import numpy as np

from src.controller.objectsController.stixController.CampaignController import get_campaign_from_camp_rel_dict
from src.controller.objectsController.stixController.ToolMalwareController import get_tool_malware_from_tw_rel_dict
from src.controller.objectsController.util import format_list_of_string, format_external_references, \
    format_related_attack_patterns, remove_empty_values
from src.model.container import IntrusionSetsContainer, AttackPatternsContainer
from src.model.interfaceToMitre.mitreData.utils.FileUtils import write_to_file
from src.model.pdfGeneration.pdf import generate_pdf_from_html


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


def __get_intrusion_set_probability_from_attack_patterns(attack_pattern_id_list):
    """
    Get the intrusion set probability from the attack pattern id list
    :param attack_pattern_id_list: the list of attack patterns
    :return: the list of (intrusion set, probability)
    """
    real_id_of_attack_pattern_list = [at.split('__')[1] for at in attack_pattern_id_list.split(',')]

    attack_patterns_list = [AttackPatternsContainer().get_object_from_data_by_mitre_id(at_id) for at_id in
                            real_id_of_attack_pattern_list]

    dict_ins_count = __get_intrusion_set_from_attack_pattern(attack_patterns_list)

    dict_ins_probability = __get_softmax_intrusion_set(dict_ins_count)

    # sort the dictionary by probability
    list_ins_prob = [[
        {
            'ID': item.x_mitre_id,
            'Name': item.name,
            'Aliases': format_list_of_string(item.aliases),
            'Domains': format_list_of_string(item.x_mitre_domains),
            'Description': item.description,
            'x_mitre_version': item.x_mitre_version,
        }, prob] for item, prob in dict_ins_probability.items()]

    list_ = list(sorted(list_ins_prob, key=lambda item: item[1], reverse=True))

    # collapse list in dict
    list_of_results = []
    for item in list_:
        dict_ = {**item[0], 'Probability': round(item[1] * 100, 2)}
        list_of_results.append(dict_)

    if len(list_of_results) > 5:
        return list_of_results[:5]

    return list_of_results


def fetch_report_of_intrusion_set_probability_from_attack_patterns(attack_pattern_id_list):
    report_data = __get_intrusion_set_probability_from_attack_patterns(attack_pattern_id_list)
    html_output = __get_intrusion_set_prob_dicts_to_html(report_data)
    filename = 'report_groups_'+datetime.now().time().strftime("%H-%M-%S")
    html_filename = filename + '.html'
    pdf_filename = filename+'.pdf'

    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'temp', 'reports'))
    write_to_file(html_output, html_filename, path)

    return generate_pdf_from_html(path+html_filename, path+pdf_filename)


def __get_intrusion_set_prob_dicts_to_html(dicts):
    # HTML document start
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Information Report</title>
        <style>
            body { font-family: 'Roboto', sans-serif; }
            h2 { text-align: center; }
            h1 { text-align: center; }
            .info-content { margin-left: 40px; margin-right: 40px; }
            p { margin-top: 4px; margin-bottom: 4px; }
        </style>
    </head>
    <body>
        <h1>Groups Detected</h1>
    """
    # Adding information based on dictionary data
    for data in dicts:
        # Format the title as "Name (ID): Probability"
        if all(key in data for key in ['Name', 'ID', 'Probability']):
            html_content += f"<h2>{data['Name']} ({data['ID']}): {data['Probability']}%</h2>"
            html_content += f"<div class='info-content'><p>{data['Description']}</p>"

            # Print additional information from the dictionary
            for key, value in data.items():
                if key not in ['Name', 'ID', 'Probability', 'Description']:  # Exclude fields used in the title
                    html_content += f"<p><strong>{key}:</strong> {value}</p>"
            html_content += "</div>"

    # HTML document end
    html_content += """
    </body>
    </html>
    """

    return html_content

def __get_softmax_intrusion_set(intrusion_set_num_of_attack_patterns):
    """
    Get the softmax of the intrusion set prediction
    :param intrusion_set_num_of_attack_patterns: dict[intrusion_set, num_of_attack_patterns]
    :return:
    """
    if not intrusion_set_num_of_attack_patterns:  # Check if the dictionary is empty
        return {}  # Return an empty dictionary or any other appropriate value

    scores = np.array(list(intrusion_set_num_of_attack_patterns.values()))
    e_x = np.exp(scores - np.max(scores))
    softmax_scores = e_x / e_x.sum(axis=0)

    return dict(zip(intrusion_set_num_of_attack_patterns.keys(), softmax_scores))


def __get_intrusion_set_from_attack_pattern(attack_pattern_list):
    """
    Get the intrusion set from the attack patterns
    :param attack_pattern_list: the list of attack pattern
    :return: the list of groups
    """
    dict_ins_count = {}
    for at in attack_pattern_list:
        ins_list = IntrusionSetsContainer().get_objects_related_by_attack_pattern_id(at.id)
        for ins in ins_list:
            if ins in dict_ins_count:
                dict_ins_count[ins] += 1
            else:
                dict_ins_count[ins] = 1

    return dict_ins_count
