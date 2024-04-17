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
    print("-------------------------",search_term)
    all_result = get_searched_obj(search_term)
    result = all_result[start:start + 15]

    return render_template('manual_search.html', result=result, page_number=page,
                           last_page_nuber=len(all_result) // MAX_OBJS_PER_PAGE, search_term=search_term)


@app.route('/util/navbar')
def navbar():
    return render_template('util/navbar.html')


@app.route('/util/file_picker')
def file_picker():
    return render_template('util/file_picker.html')


@app.route('/util/search_bar')
def search_bar():
    return render_template('util/search_bar.html')
