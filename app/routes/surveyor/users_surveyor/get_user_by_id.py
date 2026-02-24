from flask import jsonify
from sqlalchemy import text

from app.services import Session
from . import users_surveyor_bp
from .schema import user_surveyor_list_schema

@users_surveyor_bp.route('/<int:id>', methods=['GET'])
def get_user_by_id(id):
    current_session = Session()
    try:
        user = current_session.execute(
            text("SELECT * FROM tbl_user_surveyor WHERE id = :id"),
            {"id": id}
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
