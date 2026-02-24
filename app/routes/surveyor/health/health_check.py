from flask import jsonify
from . import health_bp

@health_bp.route('/', methods=['GET'])
def health_check():
    """Get all attendants for a specific task"""
    print("Health: ok")
    return jsonify({"status": "ok"})