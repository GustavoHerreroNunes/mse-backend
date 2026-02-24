from flask import jsonify, request
from sqlalchemy import text
from marshmallow import ValidationError

from app.services import Session
from . import logger, survey_pdf_bp
from .schema import survey_pdf_schema

@survey_pdf_bp.route('/<int:id_demanda>', methods=['PUT'])
def update_survey_pdf(id_demanda):
    try:
        data = survey_pdf_schema.load(request.json, partial=True)
        current_session = Session()

        try:
            # Verifica se o checklist existe
            checklist_exists = current_session.execute(
                text("SELECT id_demanda FROM tbl_status_pdf WHERE id_demanda = :id"),
                {"id": id_demanda}
            )

            if not list(checklist_exists):
                return jsonify({"error": "Status PDF not found"}), 404

            update_fields = []
            params = {"id": id_demanda}

            # Campos que podem ser atualizados
            fields_to_update = [
                "verified_by_surveyor",
                "verified_by_revisor",
                "verified_by_aprovador",
            ]

            for field in fields_to_update:
                if field in data:
                    update_fields.append(f"{field} = :{field}")
                    params[field] = data[field]

            if update_fields:
                query = f"UPDATE tbl_status_pdf SET {', '.join(update_fields)} WHERE id_demanda = :id"
                current_session.execute(text(query), params)
                current_session.commit()

                return jsonify({"message": "Status PDF updated successfully"}), 200
            else:
                return jsonify({"message": "No fields provided for update"}), 400

        except Exception as e:
            current_session.rollback()
            logger.error(f"Error updating status PDF: {str(e)}")
            return jsonify({"error": str(e)}), 500
        finally:
            current_session.close()

    except ValidationError as e:
        return jsonify({"error": "Validation Error", "details": e.messages}), 400