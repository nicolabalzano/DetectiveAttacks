from flask import Flask, render_template, request
import sys

sys.path.append('C:/Users/nikba/OneDrive/Desktop/Tesi/UniBa_Tesi')
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
    MAX_OBJS_PER_PAGE = 15
    start = page * MAX_OBJS_PER_PAGE

    search_term = request.args.get('search', '')
    all_result = get_searched_obj(search_term)

    checked_types = request.args.getlist('type')
    checked_domains = request.args.getlist('domain')

    print("checked_types: ", checked_types)
    print("checked_domains: ", checked_domains)

    # check if the user has selected any type or domain
    for types in checked_types:
        all_result = [obj for obj in all_result if obj[0].lower() == types.lower()]

    for domains in checked_domains:
        all_result = [obj for obj in all_result if obj[3].lower() == domains.lower()]

    filters = "?search=" + search_term + "&type=".join(checked_types) + "&domain=".join(checked_domains)

    result = all_result[start:start + 15]

    return render_template('manual_search.html', result=result, page_number=page,
                           last_page_nuber=len(all_result) // MAX_OBJS_PER_PAGE, filters=filters)


@app.route('/util/navbar')
def navbar():
    return render_template('util/navbar.html')


@app.route('/util/file_picker')
def file_picker():
    return render_template('util/file_picker.html')


@app.route('/util/search_bar')
def search_bar():
    return render_template('util/search_bar.html')
