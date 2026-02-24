from flask import jsonify, request
from sqlalchemy import text
from marshmallow import ValidationError

from app.services import Session
from . import demandas_bp, logger

@demandas_bp.route('/<int:demanda_id>/moving', methods=['PUT'])
def update_demanda_moving(demanda_id):
    """Update moving_to_location of a given demanda to True"""
    try:
        current_session = Session()
        try:
            # Check if demanda exists
            demanda = current_session.execute(
                text("SELECT nome_demanda FROM tbl_demandas WHERE id_demanda = :id"),
                {"id": demanda_id}
            )

            if not list(demanda):
                return jsonify({"error": "Demanda not found"}), 404

            # Update confirmation info
            current_session.execute(
                text("""
                    UPDATE tbl_demandas
                    SET moving_to_location = True
                    WHERE id_demanda = :id
                """),
                {
                    "id": demanda_id
                }
            )

            current_session.commit()

            return jsonify({"message": "Demanda moving to location info updated successfully"}), 200
        except Exception as e:
            current_session.rollback()
            logger.error(f"Error updating demanda confirmation info: {str(e)}")
            return jsonify({"error": str(e)}), 500
        finally:
            current_session.close()
    except ValidationError as e:
        return jsonify({"error": "Validation Error.", "details": e.messages})