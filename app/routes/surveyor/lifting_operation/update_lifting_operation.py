from flask import jsonify, request
from sqlalchemy import text
from marshmallow import ValidationError

from app.services import Session
from . import logger, lifting_operation_bp
from .schema import lifting_operation_schema

@lifting_operation_bp.route('/<int:cargo_id>', methods=['PUT'])
def update_lifting_operation(cargo_id):
    try:
        data = lifting_operation_schema.load(request.json, partial=True)
        current_session = Session()

        try:
            # Verifica se o cargo existe
            cargo_exists = current_session.execute(
                text("SELECT cargo_id FROM tbl_step_rigging WHERE cargo_id = :id"),
                {"id": cargo_id}
            )

            if not list(cargo_exists):
                return jsonify({"error": "Lifting operation not found"}), 404

            update_fields = []
            params = {"id": cargo_id}

            # Campos que podem ser atualizados
            fields_to_update = [
                "elements_accordance", 
                "elements_fitted", 
                "safety_devices",
                "twisted_line", 
                "slings_contact", 
                "beginning_inclination", 
                "during_inclination",
                "has_pictures_elements", 
                "has_pictures_beginning", 
                "has_pictures_overall",
                "has_pictures_stowage"
            ]

            for field in fields_to_update:
                if field in data:
                    update_fields.append(f"{field} = :{field}")
                    params[field] = data[field]

            if update_fields:
                query = f"UPDATE tbl_step_rigging SET {', '.join(update_fields)} WHERE cargo_id = :id"
                current_session.execute(text(query), params)
                current_session.commit()

                return jsonify({"message": "Lifting operation updated successfully"}), 200
            else:
                return jsonify({"message": "No fields provided for update"}), 400

        except Exception as e:
            current_session.rollback()
            logger.error(f"Error updating lifting operation: {str(e)}")
            return jsonify({"error": str(e)}), 500
        finally:
            current_session.close()

    except ValidationError as e:
        return jsonify({"error": "Validation Error", "details": e.messages}), 400