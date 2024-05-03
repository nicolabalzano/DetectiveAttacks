import os

from flask import Flask, render_template, request, jsonify
import sys


current_directory = os.path.dirname(os.path.abspath(__file__))
two_directories_up = os.path.dirname(os.path.dirname(current_directory))

sys.path.append(two_directories_up)

from flask_cors import CORS

from src.controller.objectRender.Asset import get_asset_from_mitre_id
from src.controller.objectRender.Campaign import get_campaign_from_mitre_id
from src.controller.objectRender.ToolMalware import get_tool_malware_from_mitre_id
from src.controller.objectRender.Vulnerability import get_vulnerability_from_cve_id

from src.controller.objectRender.AttackPattern import get_attack_patter_from_mitre_id
from src.controller.ManualSearch import get_searched_obj

app = Flask(__name__)

cors = CORS(app, origins='*')
list_of_filter_types = ['Attack', 'Campaign', 'Tool', 'Malware', 'Asset', 'Mapped Vulnerability']
list_of_filter_domains = ['Enterprise', 'Mobile', 'ICS', 'ATLAS', 'CVE', 'n/a']


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
def get_attack():
    searched_id = request.args.get('id')
    searched_result = get_attack_patter_from_mitre_id(searched_id)
    return searched_result


@app.route('/api/get_data/get_campaign')
def get_campaign():
    searched_id = request.args.get('id')
    searched_result = get_campaign_from_mitre_id(searched_id)
    return searched_result


@app.route('/api/get_data/get_tool_malware')
def get_tool_malware():
    searched_id = request.args.get('id')
    searched_result = get_tool_malware_from_mitre_id(searched_id)
    return searched_result


@app.route('/api/get_data/get_asset')
def get_asset():
    searched_id = request.args.get('id')
    searched_result = get_asset_from_mitre_id(searched_id)
    return searched_result


@app.route('/api/get_data/get_vulnerability')
def get_vulnerability():
    searched_id = request.args.get('id')
    searched_result = get_vulnerability_from_cve_id(searched_id)
    return searched_result
