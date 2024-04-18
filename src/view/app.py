from flask import Flask, render_template, request
import sys

sys.path.append('C:/Users/nikba/Desktop/uni/Tesi/UniBa_Tesi')
from src.controller.manualSearch import get_searched_obj

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/searching_choice')
def searching_choice():
    return render_template('searching_choice.html')


@app.route('/manual_search/<int:page>', methods=['GET'])
def manual_search_page(page):
    list_of_filter_types = ['Attack', 'Campaign', 'Tools', 'Malware', 'Asset', 'Vulnerability']
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
        print("types: ", types)
        all_result_filtered_type.extend([obj for obj in all_result if types.lower() in obj[0].lower()])

    all_result_filtered = []
    for domains in checked_domains:
        print("domains: ", domains)
        all_result_filtered.extend([obj for obj in all_result_filtered_type if domains.lower() in obj[3].lower()])

    filters = "?search=" + search_term + "&type=" + ','.join(checked_types) + "&domain=" + ','.join(checked_domains)
    print("filters: ", filters)

    result = all_result_filtered[start:start + 15]

    return render_template('manual_search.html', result=result, page_number=page,
                           last_page_nuber=len(all_result_filtered) // MAX_OBJS_PER_PAGE, list_of_filter_checked_types=checked_types, list_of_filter_types=list_of_filter_types,
                           listf_of_filter_checked_domains=checked_domains, list_of_filter_domains=list_of_filter_domains, filters=filters)


@app.route('/util/navbar')
def navbar():
    return render_template('util/navbar.html')


@app.route('/util/file_picker')
def file_picker():
    return render_template('util/file_picker.html')


@app.route('/util/search_bar')
def search_bar():
    return render_template('util/search_bar.html')
