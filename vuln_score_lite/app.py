from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

from controller.DashboardController import DashboardController
from controller.HistoryController import HistoryController

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)

dashboard_controller = DashboardController()
history_controller = HistoryController(dashboard_controller=dashboard_controller)


@app.route('/addhistory', methods=['POST'])
def add_history():
    """Add a single CVE to the current history"""
    try:
        data = request.json
        cve_id = data.get('cveId')
        
        if not cve_id:
            return jsonify({'error': 'cveId is required'}), 400
        
        result = history_controller.add_cve(cve_id)
        
        if result:
            return jsonify({'success': True, 'message': f'{cve_id} added successfully'}), 200
        else:
            return jsonify({'error': 'Failed to add CVE'}), 500
            
    except Exception as e:
        logging.error(f"Error in add_history: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/addNewCVEInList', methods=['POST'])
def add_new_cve_in_list():
    """Add a new CVE to the list (alias for add_history)"""
    return add_history()


@app.route('/addBulkCVEs', methods=['POST'])
def add_bulk_cves():
    """Add multiple CVEs to the list efficiently"""
    try:
        data = request.json
        cve_ids = data.get('cveIds', [])
        
        if not cve_ids or not isinstance(cve_ids, list):
            return jsonify({'error': 'cveIds list is required'}), 400
            
        results = history_controller.add_cves_bulk(cve_ids)
        
        return jsonify({
            'success': True, 
            'results': results,
            'message': f'Processed {len(cve_ids)} CVEs'
        }), 200
            
    except Exception as e:
        logging.error(f"Error in add_bulk_cves: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/deleteCVEFromList', methods=['POST'])
def delete_cve_from_list():
    """Remove a CVE from the list"""
    try:
        data = request.json
        cve_id = data.get('cveId')
        
        if not cve_id:
            return jsonify({'error': 'cveId is required'}), 400
            
        result = history_controller.remove_cve(cve_id)
        
        if result:
            return jsonify({'success': True, 'message': f'{cve_id} removed successfully'}), 200
        else:
            return jsonify({'success': False, 'message': 'CVE not found in list'}), 404
            
    except Exception as e:
        logging.error(f"Error in delete_cve_from_list: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/getdashboard', methods=['GET'])
def get_dashboard():
    """Get the current dashboard data"""
    try:
        result = dashboard_controller.get_dashboard()
        return jsonify(result), 200
    except Exception as e:
        logging.error(f"Error in get_dashboard: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/updatedashboard', methods=['POST'])
def update_dashboard():
    """Update dashboard score with excluded CVEs"""
    try:
        data = request.json
        excluded_list = data.get('list', [])
        mode = data.get('mode', 0)
        
        score, checked_ids = dashboard_controller.update_score(excluded_list, mode, auto_save=True)
        
        return jsonify({
            'newScore': score,
            'checkedIds': checked_ids
        }), 200
    except Exception as e:
        logging.error(f"Error in update_dashboard: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/resetdashboard', methods=['POST'])
def reset_dashboard_route():
    """Reset the dashboard by clearing all tracked CVEs and recorded score history"""
    try:
        success = dashboard_controller.reset_dashboard()
        if success:
            return jsonify({'success': True, 'message': 'Dashboard reset successfully'}), 200
        else:
            return jsonify({'success': False, 'message': 'Failed to reset dashboard'}), 500
    except Exception as e:
        logging.error(f"Error in reset_dashboard: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/score-history', methods=['GET'])
def get_score_history():
    """Get score calculation history"""
    try:
        limit = request.args.get('limit', type=int, default=None)
        history = dashboard_controller.get_score_history(limit)
        
        return jsonify({
            'success': True,
            'history': history,
            'count': len(history)
        }), 200
        
    except Exception as e:
        logging.error(f"Error in get_score_history: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/latest-scores', methods=['GET'])
def get_latest_scores():
    """Get the most recent scores without recalculating"""
    try:
        latest = dashboard_controller.score_history.get_latest_scores()
        
        if latest:
            return jsonify({
                'success': True,
                'scores': latest.get('scores', {}),
                'timestamp': latest.get('timestamp'),
                'excludedCves': latest.get('excludedCves', [])
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'No score history available. Calculate scores first.'
            }), 404
        
    except Exception as e:
        logging.error(f"Error in get_latest_scores: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)
