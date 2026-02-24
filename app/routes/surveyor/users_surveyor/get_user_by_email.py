from flask import jsonify
from sqlalchemy import text

from app.services import Session
from . import users_surveyor_bp
from .schema import user_surveyor_list_schema

@users_surveyor_bp.route('/email/<string:email>', methods=['GET'])
def get_user_by_email(email):
    current_session = Session()
    try:
        user = current_session.execute(
            text("SELECT id_user FROM tbl_user_surveyor WHERE email = :email"),
            {"email": email}
        )
        result = user_surveyor_list_schema.dump(user)

        if not result:
            return jsonify({"error": "User not found"}), 404
        
        return jsonify(result[0])
    except Exception as e:
        current_session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()
