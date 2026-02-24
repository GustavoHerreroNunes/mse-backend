from flask import jsonify, request
from sqlalchemy import text
from marshmallow import ValidationError

from app.services import Session
from . import demandas_bp, logger
from .schema import demanda_schema

@demandas_bp.route('/<int:demanda_id>/status', methods=['PUT'])
def update_demanda_status(demanda_id):
    """Update survey_status of a given demanda"""
    try:
        data = demanda_schema.load(request.json, partial=True)
        
        if not data or "survey_status" not in data:
            return jsonify({"error": "Status is required"}), 400
        
        current_session = Session()
        
        try:
            # Check if demanda exists
            demanda = current_session.execute(
                text("SELECT nome_demanda FROM tbl_demandas WHERE id_demanda = :id"),
                {"id": demanda_id}
            )
            
            if not list(demanda):
                return jsonify({"error": "Demanda not found"}), 404
            
            # Update demanda status
            current_session.execute(
                text("UPDATE tbl_demandas SET survey_status = :status WHERE id_demanda = :id"),
                {"id": demanda_id, "status": data.get("survey_status")}
            )
            
            current_session.commit()
            
            return jsonify({"message": "Demanda status updated successfully"}), 200
        except Exception as e:
            current_session.rollback()
            logger.error(f"Error updating demanda status: {str(e)}")
            return jsonify({"error": str(e)}), 500
        finally:
            current_session.close()
    except ValidationError as e:
        return jsonify({"error": "Validation Error.", "details": e.messages})