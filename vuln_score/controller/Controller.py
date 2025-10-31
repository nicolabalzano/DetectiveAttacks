from flask import Flask, request, abort
from flask_cors import CORS, cross_origin
import sys
sys.path.append('src')
import os
import controller.DashboardController as dc
import controller.SearchController as sc
import controller.HistoryController as hc
import controller.ConvertController as cc
import controller.NewResearchController as nc
import controller.UserProfileController as uc
import controller.HomeController as homecontroller
from controller.utils.ControllerUitls import check_cve, check_cvss, check_cwe
import logging

__app = Flask("score_plus")
__cors = CORS(__app)
__app.config['CORS_HEADERS'] = 'Content-Type'


@__app.route('/api/gethistory', methods=['GET'])
@cross_origin()
def get_history():
    args = request.args.to_dict()
    logging.debug(args)

    if len(args) == 0:
        return hc._get_history()

    for arg in args:
        if arg == 'keyword':
            print(args[arg])
            return hc._search_history_id(args[arg])
    
    abort(400) # No matching function found


@__app.route('/api/addhistory', methods=['GET'])
@cross_origin()
def add_history():
    args = request.args.to_dict()
    logging.debug(args)

    if len(args) == 0:   
        abort(403)

    for arg in args:
        if arg == 'cveId':
            result = hc._add_history(nc._new_research(args[arg] if check_cve(args[arg]) else abort(400)))
            return {'success': result}

    abort(400) # No matching function found


@__app.route('/api/getdashboard', methods=['GET'])
@cross_origin()
def get_dashboard():
    return dc._get_dashboard()


@__app.route('/api/updatedashboard', methods=['POST'])
@cross_origin()
def update_dashboard():
    data = request.json['list']
    mode = request.json['mode']

    score, checked_ids = dc._update_score(data, mode)
    return {'newScore': score, 'checkedIds': checked_ids}


@__app.route('/api/getcwe', methods=['GET'])
@cross_origin()
def get_cwe():
    args = request.args.to_dict()
    logging.debug(args)

    if len(args) == 0:
        abort(403)
    
    for arg in args:
        if arg == 'cweId':
            return dc._get_cwe(args[arg] if check_cwe(args[arg]) else abort(400))


@__app.route('/api/getcve', methods=['GET'])
@cross_origin()
def get_cve():
    args = request.args.to_dict()
    logging.debug(args)

    if len(args) == 0:
        abort(403)
    
    for arg in args:
        if arg == 'cveId':
            return sc._get_cve_from_id(args[arg]) if check_cve(args[arg]) else abort(400)
        
    abort(400) # No matching function found


@__app.route('/api/convertcvss', methods=['GET'])
@cross_origin()
def convert_cvss():
    args = request.args.to_dict()
    logging.debug(args)

    if len(args) == 0:
        abort(403)

    for arg in args:
        if arg == 'vector':
            return cc._convert_cvss_to_v4(args[arg]) if check_cvss(args[arg]) else abort(400)
    
    abort(400) # No matching function found


@__app.route('/api/cvssdata', methods=['GET'])
@cross_origin()
def get_cvss_data():
    args = request.args.to_dict()
    logging.debug(args)

    if len(args) == 0:
        abort(403)

    for arg in args:
        if arg == 'vector':
            print(check_cvss(args[arg]))
            return cc._get_cvss_data(args[arg]) if check_cvss(args[arg]) else abort(400)
    
    abort(400) # No matching function found


@__app.route('/api/getassets', methods=['GET'])
@cross_origin()
def get_assets():
    return uc._get_assets()


@__app.route('/api/updateassets', methods=['POST'])
@cross_origin()
def update_assets():
    data = request.json['assets']
    return uc._update_assets(data)


@__app.route('/api/getcwecount', methods=['GET'])
@cross_origin()
def get_cwe_count():
    return homecontroller._get_cwe_count()


@__app.route('/api/getcvecount', methods=['GET'])
@cross_origin()
def get_cve_count():
    return homecontroller._get_cve_count()


# App start up
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 7777))
    __app.run(host='0.0.0.0', port=port, debug=True)
