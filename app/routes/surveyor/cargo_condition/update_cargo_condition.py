from flask import jsonify, request
from sqlalchemy import text
from marshmallow import ValidationError

from app.services import Session
from . import logger, cargo_condition_bp
from .schema import cargo_condition_schema

@cargo_condition_bp.route('/<int:cargo_id>', methods=['PUT'])
def update_cargo_condition(cargo_id):
    try:
        data = cargo_condition_schema.load(request.json, partial=True)
        current_session = Session()

        try:
            # Verifica se o cargo existe
            cargo_exists = current_session.execute(
                text("SELECT cargo_id FROM tbl_cargo_condition WHERE cargo_id = :id"),
                {"id": cargo_id}
            )

            if not list(cargo_exists):
                return jsonify({"error": "Cargo condition not found"}), 404

            update_fields = []
            params = {"id": cargo_id}

            # Campos que podem ser atualizados
            fields_to_update = [
                "well_received",
                "instruction",
                "external_condition",
                "packing",
                "identification_condition",
                "protection",
                "stability",
                "cleanliness",
                "integrity",
                "warning_labels",
                "markings",
                "moisture",
                "weight_distribution",
                "stacking",
                "shifting"
            ]

            for field in fields_to_update:
                if field in data:
                    update_fields.append(f"{field} = :{field}")
                    params[field] = data[field]

            if update_fields:
                query = f"UPDATE tbl_cargo_condition SET {', '.join(update_fields)} WHERE cargo_id = :id"
                current_session.execute(text(query), params)
                current_session.commit()

                return jsonify({"message": "Cargo condition updated successfully"}), 200
            else:
                return jsonify({"message": "No fields provided for update"}), 400

        except Exception as e:
            current_session.rollback()
            logger.error(f"Error updating cargo: {str(e)}")
            return jsonify({"error": str(e)}), 500
        finally:
            current_session.close()

    except ValidationError as e:
        return jsonify({"error": "Validation Error", "details": e.messages}), 400