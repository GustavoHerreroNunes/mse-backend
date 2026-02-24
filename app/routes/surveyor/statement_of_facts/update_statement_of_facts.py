from flask import jsonify, request
from sqlalchemy import text
from marshmallow import ValidationError

from app.services import Session
from . import logger, statement_of_facts_bp
from .schema import statement_of_facts_schema

@statement_of_facts_bp.route('/<int:event_id>', methods=['PUT'])
def update_statement_of_facts(event_id):
    try:
        data = statement_of_facts_schema.load(request.json, partial=True)
        current_session = Session()

        try:
            # Verifica se o registro existe
            record_exists = current_session.execute(
                text("SELECT event_id FROM tbl_statement WHERE event_id = :id"),
                {"id": event_id}
            )

            if not list(record_exists):
                return jsonify({"error": "Statement of facts not found"}), 404

            update_fields = []
            params = {"id": event_id}

            # Campos que podem ser atualizados
            fields_to_update = [
                "location", "preliminary_status", "preliminary_timestamp_start",
                "location_status", "location_timestamp_start", "task_status", "task_timestamp_start",
                "ship_status", "ship_timestamp_start", "attendance_status", "attendance_timestamp_start",
                "cargo_status", "cargo_timestamp_start", "preliminary_timestamp_end", "location_timestamp_end",
                "task_timestamp_end", "ship_timestamp_end", "attendance_timestamp_end", "cargo_timestamp_end"
            ]

            for field in fields_to_update:
                if field in data:
                    update_fields.append(f"{field} = :{field}")
                    params[field] = data[field]

            if update_fields:
                query = f"UPDATE tbl_statement SET {', '.join(update_fields)} WHERE event_id = :id"
                current_session.execute(text(query), params)
                current_session.commit()

                return jsonify({"message": "Statement of facts updated successfully"}), 200
            else:
                return jsonify({"message": "No fields provided for update"}), 400

        except Exception as e:
            current_session.rollback()
            logger.error(f"Error updating statement of facts: {str(e)}")
            return jsonify({"error": str(e)}), 500
        finally:
            current_session.close()

    except ValidationError as e:
        return jsonify({"error": "Validation Error", "details": e.messages}), 400
