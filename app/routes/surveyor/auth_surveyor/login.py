from flask import request, jsonify
from sqlalchemy import text
from app.services import Session
from werkzeug.security import check_password_hash

from . import auth_surveyor_bp

@auth_surveyor_bp.route('/login', methods=['POST'])
def login():
    data = request.json

    if not data.get("email") or not data.get("password"):
        return jsonify({"error": "Request Requirements not met: Email and Password are required."}), 400

    current_session = Session()

    try:
        user = current_session.execute(
            text("SELECT id, password FROM tbl_user_surveyor WHERE email = :email"),
            {"email": data.get("email")}
        )

        if not user:
            return jsonify({"error": "Invalid credentials"}), 401
        
        dict_user = [dict(row) for row in user.mappings()][0]

        if check_password_hash(dict_user["password"], data.get("password")):
            return jsonify({
                "message": "User authorized",
                "user_id": dict_user["id"]
            }), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    except Exception as e:
        current_session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()