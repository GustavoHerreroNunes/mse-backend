from flask import jsonify
from sqlalchemy import text

from app.services import Session
from . import users_surveyor_bp

@users_surveyor_bp.route('/<int:id>', methods=['DELETE'])
def delete_user(id):
    current_session = Session()
    try:
        user = current_session.execute(
            text("SELECT id FROM tbl_user_surveyor WHERE id = :id"),
            {"id": id}
        )
        if not list(user):
            return jsonify({"error": "User not found"}), 404
        
        current_session.execute(
            text("DELETE FROM tbl_user_surveyor WHERE id = :id"),
            {"id": id}
        )

        current_session.commit()

        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        current_session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()
