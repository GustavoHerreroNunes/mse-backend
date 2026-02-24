from flask import jsonify, request
from sqlalchemy import text
from marshmallow import ValidationError

from app.services import Session
from . import logger, cargo_storage_bp
from .schema import cargo_storage_schema

@cargo_storage_bp.route('/<int:cargo_id>', methods=['PUT'])
def update_cargo_storage(cargo_id):
    try:
        data = cargo_storage_schema.load(request.json, partial=True)
        current_session = Session()

        try:
            # Verifica se o cargo existe
            cargo_exists = current_session.execute(
                text("SELECT cargo_id FROM tbl_step_storage WHERE cargo_id = :id"),
                {"id": cargo_id}
            )

            if not list(cargo_exists):
                return jsonify({"error": "Cargo storage not found"}), 404

            update_fields = []
            params = {"id": cargo_id}

            # Campos que podem ser atualizados
            fields_to_update = [
                "proper_stowage", 
                "obstructions_stowage", 
                "proper_plating",
                "surrounded_risks", 
                "damages_internal", 
                "contaminant"
            ]

            for field in fields_to_update:
                if field in data:
                    update_fields.append(f"{field} = :{field}")
                    params[field] = data[field]

            if update_fields:
                query = f"UPDATE tbl_step_storage SET {', '.join(update_fields)} WHERE cargo_id = :id"
                current_session.execute(text(query), params)
                current_session.commit()

                return jsonify({"message": "Cargo storage updated successfully"}), 200
            else:
                return jsonify({"message": "No fields provided for update"}), 400

        except Exception as e:
            current_session.rollback()
            logger.error(f"Error updating cargo storage: {str(e)}")
            return jsonify({"error": str(e)}), 500
        finally:
            current_session.close()

    except ValidationError as e:
        return jsonify({"error": "Validation Error", "details": e.messages}), 400