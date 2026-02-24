from flask import request, jsonify
from sqlalchemy import text
from marshmallow import ValidationError
from app.services import Session
from . import statement_of_facts_bp, logger
from .schema import statement_of_facts_schema

@statement_of_facts_bp.route('/', methods=['POST'])
def add_statement_of_facts():
    """Add new statement of facts entry"""
    try:
        data = statement_of_facts_schema.load(request.json)
        current_session = Session()

        try:

            # Verifica se o registro existe
            record_exists = current_session.execute(
                text("SELECT event_id FROM tbl_statement WHERE demanda_id = :id"),
                {"id": data.get("demanda_id")}
            )

            if list(record_exists):
                return jsonify({"error": "Statement of facts already exists"}), 409
            
            # Campos disponíveis para inserção
            fields_to_insert = [
                "demanda_id", "location", "preliminary_status", "preliminary_timestamp_start",
                "location_status", "location_timestamp_start", "task_status", "task_timestamp_start",
                "ship_status", "ship_timestamp_start", "attendance_status", "attendance_timestamp_start",
                "cargo_status", "cargo_timestamp_start", "preliminary_timestamp_end", "location_timestamp_end",
                "task_timestamp_end", "ship_timestamp_end", "attendance_timestamp_end", "cargo_timestamp_end"
            ]

            insert_fields = []
            insert_values = []
            params = {}

            for field in fields_to_insert:
                if field in data and data[field] is not None:
                    insert_fields.append(field)
                    insert_values.append(f":{field}")
                    params[field] = data[field]

            # Validar campos obrigatórios
            required_fields = ["demanda_id"]
            for field in required_fields:
                if field not in params:
                    return jsonify({"error": f"Required field missing: {field}"}), 400

            query = f"""
                INSERT INTO tbl_statement ({', '.join(insert_fields)})
                VALUES ({', '.join(insert_values)})
                RETURNING event_id
            """

            result = current_session.execute(text(query), params)
            current_session.commit()

            event_id = result.fetchone()._mapping["event_id"]

            return jsonify({
                "message": "Statement of facts entry created successfully",
                "id": event_id
            }), 201

        except Exception as e:
            current_session.rollback()
            logger.error(f"Error creating statement of facts: {str(e)}")
            return jsonify({"error": str(e)}), 500
        finally:
            current_session.close()

    except ValidationError as e:
        return jsonify({"error": "Validation Error", "details": e.messages}), 400
