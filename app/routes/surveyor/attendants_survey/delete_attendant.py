from flask import jsonify
from sqlalchemy import text
from app.services import Session
from . import attendants_survey_bp

@attendants_survey_bp.route('/<int:attendant_id>', methods=['DELETE'])
def delete_attendant(attendant_id):
    """Delete an attendant by id"""
    current_session = Session()
    try:
        attendant = current_session.execute(
            text("SELECT id_attendant FROM tbl_attendant_survey_boarding WHERE id_attendant = :id"),
            {"id": attendant_id}
        )
        if not list(attendant):
            return jsonify({"error": "Attendant not found"}), 404

        current_session.execute(
            text("DELETE FROM tbl_attendant_survey_boarding WHERE id_attendant = :id"),
            {"id": attendant_id}
        )
        current_session.commit()
        return jsonify({"message": "Attendant deleted successfully"}), 200
    except Exception as e:
        current_session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()
