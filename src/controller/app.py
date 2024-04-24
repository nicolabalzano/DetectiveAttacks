from flask import Flask, render_template, request, jsonify
import sys

from flask_cors import CORS

# sys.path.append('C:/Users/nikba/Desktop/uni/Tesi/DetectiveAttack')
sys.path.append('C:/Users/nikba/OneDrive/Desktop/Tesi/DetectiveAttack')

from src.controller.objectRender.attackPattern import get_attack_patter_from_mitre_id
from src.controller.manualSearch import get_searched_obj

app = Flask(__name__)

cors = CORS(app, origins='*')
list_of_filter_types = ['Attack', 'Campaign', 'Tool', 'Malware', 'Asset', 'Vulnerability']
list_of_filter_domains = ['Enterprise', 'Mobile', 'ICS', 'ATLAS', 'CVE', 'n/a']

# Important attributes to show in the mirror info rectangle
LIST_OF_IMPORTANT_ATTRS = ['ID', 'Domains', 'Mitre Kill Chain phases', 'Kill Chain phases', 'Platforms', 'Deprecated']

# Attributes already shown
LIST_OF_ALREADY_SHOWN_ATTRS = LIST_OF_IMPORTANT_ATTRS + ['Name', 'Type', 'Description', 'Detection suggestions',
                                                         'Mitigations', 'Procedure examples']


@app.template_filter('remove_important_attr_to_dict')
def remove_important_attr_to_dict(my_dict):
    """Remove important attributes from dict"""
    for important_attr in LIST_OF_ALREADY_SHOWN_ATTRS:
        my_dict.pop(important_attr, None)

    return my_dict


@app.template_filter('get_dict_with_info_attr')
def get_dict_with_info_attr(my_dict):
    """Return dict with items for mirror info rectangle"""
    dict_of_info = {}
    for important_attr in LIST_OF_IMPORTANT_ATTRS:
        if important_attr in my_dict:
            dict_of_info[important_attr] = my_dict[important_attr]

    return dict_of_info


@app.route('/api/get_filters', methods=["GET"])
def get_filters():
    return jsonify({
        'list_of_filter_types': list_of_filter_types,
        'list_of_filter_domains': list_of_filter_domains})


@app.route('/api/get_data', methods=["GET"])
def get_data():
    search_terms = request.args.get('search')
    checked_types = request.args.get('types')
    checked_domains = request.args.get('domains')

    all_result = get_searched_obj(search_terms)

    # if the user has not selected any type or domain, the default value is ['----'] so nothing matches
    if not checked_domains:
        checked_domains = ['----']
    elif checked_domains == 'all':
        checked_domains = list_of_filter_domains
    else:
        checked_domains = checked_domains.split(',')

    if not checked_types:
        checked_types = ['----']
    elif checked_types == 'all':
        checked_types = list_of_filter_types
    else:
        checked_types = checked_types.split(',')

    # check if the user has selected any type or domain
    all_result_filtered_type = []
    for types in checked_types:
        all_result_filtered_type.extend([obj for obj in all_result if types.lower() in obj[0].lower()])

    all_result_filtered = []
    for domains in checked_domains:
        all_result_filtered.extend([obj for obj in all_result_filtered_type if domains.lower() in obj[3].lower()])

    results = all_result_filtered

    # filters = "?search=" + search_term + "&type=" + ','.join(checked_types) + "&domain=" + ','.join(checked_domains)

    return jsonify({
        'results': results,
    })
    # , filters=filters


@app.route('/api/get_data/get_attack')
def attack_pattern():
    searched_id = request.args.get('id')
    searched_result = get_attack_patter_from_mitre_id(searched_id)
    return searched_result
