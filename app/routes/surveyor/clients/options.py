from flask import jsonify
from . import clients_bp

@clients_bp.route('/options', methods=['OPTIONS'])
def options():
    return jsonify({'status': 'OK'}), 200
