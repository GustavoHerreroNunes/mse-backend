from flask import jsonify, request
from sqlalchemy import text
from marshmallow import ValidationError

from app.services import Session
from . import logger, statement_of_facts_bp
from .schema import statement_of_facts_cargo_schema

@statement_of_facts_bp.route('/cargo/<int:event_id>', methods=['PUT'])
def update_statement_of_facts_cargo(event_id):
    try:
        data = statement_of_facts_cargo_schema.load(request.json, partial=True)
        current_session = Session()

        try:
            # Verifica se o registro existe
            record_exists = current_session.execute(
                text("SELECT event_id FROM tbl_statement_cargo WHERE event_id = :id"),
                {"id": event_id}
            )

            if not list(record_exists):
                return jsonify({"error": "Statement of facts not found"}), 404

            update_fields = []
            params = {"id": event_id}

            # Campos que podem ser atualizados
            fields_to_update = [
                "location", "inspection_status", "inspection_timestamp_start",
                "items_status", "items_timestamp_start", "operation_status", "operation_timestamp_start",
                "storage_status", "storage_timestamp_start", "material_status", "material_timestamp_start",
                "board_status", "board_timestamp_start", "inspection_timestamp_end", "items_timestamp_end",
                "operation_timestamp_end", "storage_timestamp_end", "material_timestamp_end", "board_timestamp_end"
            ]

            for field in fields_to_update:
                if field in data:
                    update_fields.append(f"{field} = :{field}")
                    params[field] = data[field]

            if update_fields:
                query = f"UPDATE tbl_statement_cargo SET {', '.join(update_fields)} WHERE event_id = :id"
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
