import os

from flask import Flask, render_template, request, jsonify
import sys

from src.controller.objectsController.stixController.IntrusionSetController import get_intrusion_set_from_mitre_id

current_directory = os.path.dirname(os.path.abspath(__file__))
two_directories_up = os.path.dirname(os.path.dirname(current_directory))

sys.path.append(two_directories_up)

from flask_cors import CORS

from src.controller.objectsController.stixController.AssetController import get_asset_from_mitre_id
from src.controller.objectsController.stixController.CampaignController import get_campaign_from_mitre_id
from src.controller.objectsController.stixController.ToolMalwareController import get_tool_malware_from_mitre_id
from src.controller.objectsController.VulnerabilityController import get_vulnerability_from_cve_id

from src.controller.objectsController.stixController.AttackPatternController import get_attack_patter_from_mitre_id, \
    get_all_attack_patterns_grouped_by_CKCP, get_all_platforms
from src.controller.ManualSearch import get_searched_obj

app = Flask(__name__)

cors = CORS(app, origins='*')
DICT_OF_FILTER_TYPES = {
    'Attack': 'attack-pattern',
    'Campaign': 'campaign',
    'Tool': 'tool',
    'Malware': 'malware',
    'Asset': 'x-mitre-asset',
    'Group': 'intrusion-set',
    'Mapped Vulnerability': 'mapped_vulnerability'
}

LIST_OF_FILTER_MITRE_DOMAINS = ['Enterprise', 'Mobile', 'ICS', 'ATLAS']
LIST_OF_FILTER_DOMAINS = LIST_OF_FILTER_MITRE_DOMAINS + ['CVE', 'CWE', 'n/a']

@app.route('/api/get_filters', methods=["GET"])
def get_filters():
    return jsonify({
        'list_of_filter_types': list(DICT_OF_FILTER_TYPES.keys()),
        'list_of_filter_domains': LIST_OF_FILTER_DOMAINS})


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
        checked_domains = LIST_OF_FILTER_DOMAINS
    else:
        checked_domains = checked_domains.split(',')

    if not checked_types:
        checked_types = ['----']
    elif checked_types == 'all':
        checked_types = DICT_OF_FILTER_TYPES.values()
    else:
        checked_types = checked_types.split(',')
        checked_types = [DICT_OF_FILTER_TYPES[types] for types in checked_types]

    # filter the result by the types
    all_result_filtered_type = []
    for types in checked_types:
        all_result_filtered_type.extend([obj for obj in all_result if types.lower() in obj[0].lower()])

    # filter the result by the domains
    all_result_filtered = []
    for domains in checked_domains:
        all_result_filtered.extend([obj for obj in all_result_filtered_type if domains.lower() in obj[3].lower()])

    results = all_result_filtered

    # filters = "?search=" + search_term + "&type=" + ','.join(checked_types) + "&domain=" + ','.join(checked_domains)

    return jsonify({
        'results': results,
    })
    # , filters=filters


@app.route('/api/get_data/get_attack_pattern', methods=["GET"])
def get_attack_pattern():
    searched_id = request.args.get('id')
    searched_result = get_attack_patter_from_mitre_id(searched_id)
    return searched_result


@app.route('/api/get_data/get_attack_patterns_grouped_by_CKCP', methods=["GET"])
def get_attack_patterns_grouped_by_CKCP():
    """
    Get all attack patterns grouped by CKC phases
    :return: dict of {CKC_phase: [attack_pattern]}
    """
    return get_all_attack_patterns_grouped_by_CKCP()


@app.route('/api/get_data/get_campaign', methods=["GET"])
def get_campaign():
    searched_id = request.args.get('id')
    searched_result = get_campaign_from_mitre_id(searched_id)
    return searched_result


@app.route('/api/get_data/get_tool_malware', methods=["GET"])
def get_tool_malware():
    searched_id = request.args.get('id')
    searched_result = get_tool_malware_from_mitre_id(searched_id)
    return searched_result


@app.route('/api/get_data/get_asset', methods=["GET"])
def get_asset():
    searched_id = request.args.get('id')
    searched_result = get_asset_from_mitre_id(searched_id)
    return searched_result


@app.route('/api/get_data/get_intrusion_set', methods=["GET"])
def get_intrusion_set():
    searched_id = request.args.get('id')
    searched_result = get_intrusion_set_from_mitre_id(searched_id)
    return searched_result


@app.route('/api/get_data/get_vulnerability', methods=["GET"])
def get_vulnerability():
    searched_id = request.args.get('id')
    searched_result = get_vulnerability_from_cve_id(searched_id)
    return searched_result


@app.route('/api/get_data/get_platforms', methods=["GET"])
def get_platforms():
    """
    Get all platforms
    :return: list of platforms
    """
    return get_all_platforms()


@app.route('/api/get_data/get_domains', methods=["GET"])
def get_domains():
    return LIST_OF_FILTER_MITRE_DOMAINS
