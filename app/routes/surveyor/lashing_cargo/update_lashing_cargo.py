from flask import jsonify, request
from sqlalchemy import text
from marshmallow import ValidationError

from app.services import Session
from . import logger, lashing_cargo_bp
from .schema import lashing_cargo_schema

@lashing_cargo_bp.route('/<int:cargo_id>', methods=['PUT'])
def update_lashing_cargo(cargo_id):
    try:
        data = lashing_cargo_schema.load(request.json, partial=True)
        current_session = Session()

        try:
            # Verifica se o cargo existe
            cargo_exists = current_session.execute(
                text("SELECT cargo_id FROM tbl_step_lashing WHERE cargo_id = :id"),
                {"id": cargo_id}
            )

            if not list(cargo_exists):
                return jsonify({"error": "Lashing cargo not found"}), 404

            update_fields = []
            params = {"id": cargo_id}

            # Campos que podem ser atualizados
            fields_to_update = [
                "seafastened", 
                "materials", 
                "lines_connected",
                "lines_tighten", 
                "lines_protection", 
                "welded_stoppers",
                "welded_rings", 
                "fitted_stoppers", 
                "structure_failure",
                "approved_crew"
            ]

            for field in fields_to_update:
                if field in data:
                    update_fields.append(f"{field} = :{field}")
                    params[field] = data[field]

            if update_fields:
                query = f"UPDATE tbl_step_lashing SET {', '.join(update_fields)} WHERE cargo_id = :id"
                current_session.execute(text(query), params)
                current_session.commit()

                return jsonify({"message": "Lashing cargo updated successfully"}), 200
            else:
                return jsonify({"message": "No fields provided for update"}), 400

        except Exception as e:
            current_session.rollback()
            logger.error(f"Error updating lashing cargo: {str(e)}")
            return jsonify({"error": str(e)}), 500
        finally:
            current_session.close()

    except ValidationError as e:
        return jsonify({"error": "Validation Error", "details": e.messages}), 400