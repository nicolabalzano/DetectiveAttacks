import os

from flask import Flask, request, jsonify
import sys
from flask_cors import CORS

current_directory = os.path.dirname(os.path.abspath(__file__))
two_directories_up = os.path.dirname(os.path.dirname(current_directory))

sys.path.append(two_directories_up)


from src.CapecData import CapecData
from src.utils.FetchData import fetch_capec_data

__app = Flask(__name__)
__app.config["JSON_SORT_KEYS"] = False
CORS(__app)

fetch_capec_data()

@__app.route('/get_capec', methods=["GET"])
def get_capec():
    capec_id = request.args.get('id')
    capec_data = CapecData().get_capec_by_capec_id(capec_id)
    return jsonify(capec_data)


@__app.route('/get_attack_patterns_mitre_ids_by_capec', methods=["GET"])
def get_attack_patterns_mitre_ids_by_CAPEC():
    capec_id = request.args.get('id')
    attack_patterns_mitre_ids = CapecData().get_attack_patterns_mitre_id_by_CAPEC(capec_id)
    return jsonify(attack_patterns_mitre_ids)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5003))
    __app.run(host='0.0.0.0', port=port, debug=True)