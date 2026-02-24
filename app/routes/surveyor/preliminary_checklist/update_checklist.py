from flask import jsonify, request
from sqlalchemy import text
from marshmallow import ValidationError

from app.services import Session
from . import logger, checklist_bp
from .schema import checklist_schema

@checklist_bp.route('/<int:id_survey>', methods=['PUT'])
def update_checklist(id_survey):
    try:
        data = checklist_schema.load(request.json, partial=True)
        current_session = Session()

        try:
            # Verifica se o checklist existe
            checklist_exists = current_session.execute(
                text("SELECT id_survey FROM tbl_preliminary_checklist WHERE id_survey = :id"),
                {"id": id_survey}
            )

            if not list(checklist_exists):
                return jsonify({"error": "Preliminary checklist not found"}), 404

            update_fields = []
            params = {"id": id_survey}

            # Campos que podem ser atualizados
            fields_to_update = [
                "received_packing", 
                "loi", 
                "received_lifting",
                "received_stowage", 
                "received_seafastening", 
                "contact_terminal",
                "contact_port", 
                "contact_vessel", 
                "is_finished"
            ]

            for field in fields_to_update:
                if field in data:
                    update_fields.append(f"{field} = :{field}")
                    params[field] = data[field]

            if update_fields:
                query = f"UPDATE tbl_preliminary_checklist SET {', '.join(update_fields)} WHERE id_survey = :id"
                current_session.execute(text(query), params)
                current_session.commit()

                return jsonify({"message": "Preliminary checklist updated successfully"}), 200
            else:
                return jsonify({"message": "No fields provided for update"}), 400

        except Exception as e:
            current_session.rollback()
            logger.error(f"Error updating preliminary checklist: {str(e)}")
            return jsonify({"error": str(e)}), 500
        finally:
            current_session.close()

    except ValidationError as e:
        return jsonify({"error": "Validation Error", "details": e.messages}), 400