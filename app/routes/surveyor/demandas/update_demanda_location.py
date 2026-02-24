from flask import jsonify, request
from sqlalchemy import text
from marshmallow import ValidationError

from app.services import Session
from . import demandas_bp, logger

@demandas_bp.route('/<int:demanda_id>/location', methods=['PUT'])
def update_demanda_location(demanda_id):
    """Update location_confirmation and time_confirmation of a given demanda and define have_arrived equal to one"""
    try:
        data = request.get_json()
        time_confimation = data.get("time_confirmation")
        location_confirmation = data.get("location_confirmation")

        if not time_confimation or not location_confirmation:
            return jsonify({"error": "Missing required fields"}), 400

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
                    SET have_arrived = True,
                        time_confimation = :time_confimation,
                        location_confirmation = :location_confirmation
                    WHERE id_demanda = :id
                """),
                {
                    "id": demanda_id,
                    "time_confimation": time_confimation,
                    "location_confirmation": location_confirmation
                }
            )

            current_session.commit()

            return jsonify({"message": "Demanda confirmation info updated successfully"}), 200
        except Exception as e:
            current_session.rollback()
            logger.error(f"Error updating demanda confirmation info: {str(e)}")
            return jsonify({"error": str(e)}), 500
        finally:
            current_session.close()
    except ValidationError as e:
        return jsonify({"error": "Validation Error.", "details": e.messages})