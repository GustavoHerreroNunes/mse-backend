from flask import request, jsonify
from sqlalchemy import text
from marshmallow import ValidationError
from app.services import Session
from . import statement_of_facts_bp, logger
from .schema import statement_of_facts_cargo_schema

@statement_of_facts_bp.route('/cargo/', methods=['POST'])
def add_statement_of_facts_cargo():
    """Add new statement of facts entry"""
    try:
        data = statement_of_facts_cargo_schema.load(request.json)
        current_session = Session()

        try:
            # Verifica se o registro existe
            record_exists = current_session.execute(
                text("SELECT event_id FROM tbl_statement_cargo WHERE cargo_id = :id"),
                {"id": data.get("cargo_id")}
            )

            if list(record_exists):
                return jsonify({"error": "Statement of facts already exists"}), 409
            
            # Campos disponíveis para inserção
            fields_to_insert = [
                "cargo_id", "location", "inspection_status", "inspection_timestamp_start",
                "items_status", "items_timestamp_start", "operation_status", "operation_timestamp_start",
                "storage_status", "storage_timestamp_start", "material_status", "material_timestamp_start",
                "board_status", "board_timestamp_start", "inspection_timestamp_end", "items_timestamp_end",
                "operation_timestamp_end", "storage_timestamp_end", "material_timestamp_end", "board_timestamp_end"
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
            required_fields = ["cargo_id"]
            for field in required_fields:
                if field not in params:
                    return jsonify({"error": f"Required field missing: {field}"}), 400

            query = f"""
                INSERT INTO tbl_statement_cargo ({', '.join(insert_fields)})
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
