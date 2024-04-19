from flask import Flask, render_template, request
import sys

# sys.path.append('C:/Users/nikba/Desktop/uni/Tesi/UniBa_Tesi')
sys.path.append('C:/Users/nikba/OneDrive/Desktop/Tesi/UniBa_Tesi')

from src.controller.objectRender.attackPattern import get_attack_patter_from_mitre_id
from src.controller.manualSearch import get_searched_obj

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/searching_choice')
def searching_choice():
    return render_template('searching_choice.html')


@app.route('/manual_search/<int:page>', methods=['GET'])
def manual_search(page):
    list_of_filter_types = ['Attack', 'Campaign', 'Tool', 'Malware', 'Asset', 'Vulnerability']
    list_of_filter_domains = ['Enterprise', 'Mobile', 'ICS', 'ATLAS', 'CVE', 'n/a']
    MAX_OBJS_PER_PAGE = 15
    start = page * MAX_OBJS_PER_PAGE

    search_term = request.args.get('search', '')
    all_result = get_searched_obj(search_term)

    checked_types = request.args.get('type')
    checked_domains = request.args.get('domain')

    # if the user has not selected any type or domain, the default value is ['']
    if not checked_domains:
        checked_domains = ['']
    else:
        checked_domains = checked_domains.split(',')

    if not checked_types:
        checked_types = ['']
    else:
        checked_types = checked_types.split(',')

    # check if the user has selected any type or domain
    all_result_filtered_type = []
    for types in checked_types:
        all_result_filtered_type.extend([obj for obj in all_result if types.lower() in obj[0].lower()])

    all_result_filtered = []
    for domains in checked_domains:
        all_result_filtered.extend([obj for obj in all_result_filtered_type if domains.lower() in obj[3].lower()])

    filters = "?search=" + search_term + "&type=" + ','.join(checked_types) + "&domain=" + ','.join(checked_domains)

    result = all_result_filtered[start:start + 15]

    return render_template('manual_search.html', result=result, page_number=page,
                           last_page_nuber=len(all_result_filtered) // MAX_OBJS_PER_PAGE,
                           list_of_filter_checked_types=checked_types, list_of_filter_types=list_of_filter_types,
                           listf_of_filter_checked_domains=checked_domains,
                           list_of_filter_domains=list_of_filter_domains, filters=filters)


@app.route('/attack_pattern/<string:searched_id>')
def attack_pattern(searched_id):
    searched_result = get_attack_patter_from_mitre_id(searched_id)
    return render_template('attack_pattern.html', searched_result=searched_result)


@app.route('/util/navbar')
def navbar():
    return render_template('util/navbar.html')


@app.route('/util/file_picker')
def file_picker():
    return render_template('util/file_picker.html')


@app.route('/util/search_bar')
def search_bar():
    return render_template('util/search_bar.html')


@app.route('/util/object_shower_function')
def object_shower_function():
    return render_template('util/object_shower_function.html')


# custom filter
@app.template_filter('all_empty')
def all_empty(s):
    return all(x == '' for x in s)


@app.template_filter('is_list')
def is_list(value):
    return isinstance(value, list)


# Important attributes to show in the mirror info rectangle
LIST_OF_IMPORTANT_ATTRS = ['ID', 'Domains', 'Mitre Kill Chain phases', 'Kill Chain phases', 'Platforms', 'Deprecated']

# Attributes already shown
LIST_OF_ALREADY_SHOWN_ATTRS = LIST_OF_IMPORTANT_ATTRS + ['Name', 'Type', 'Description', 'Detection suggestions', 'Mitigations', 'Procedure examples']


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

