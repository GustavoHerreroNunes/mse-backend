from flask import request, jsonify
from sqlalchemy import text
from app.services import Session
from . import cargo_bp, logger
from .schema import cargo_schema

@cargo_bp.route('/', methods=['POST'])
def add_cargo():
    """Add new cargo"""
    data = cargo_schema.load(request.json)
    current_session = Session()

    try:
        # Verifica se a task existe
        task_result = current_session.execute(
            text("SELECT id_task FROM tbl_task_survey_boarding WHERE id_task = :id"),
            {"id": data.get("id_task")}
        )

        if not list(task_result):
            return jsonify({"error": "Task not found"}), 404

        # Campos disponíveis para inserção
        fields_to_insert = [
            "cargo_name",
            "id_task",
            "cargo_type",
            "weight",
            "length",
            "width",
            "height",
            "extra_info"
        ]

        insert_fields = []
        insert_values = []
        params = {}

        for field in fields_to_insert:
            if field in data:
                insert_fields.append(field)
                insert_values.append(f":{field}")
                params[field] = data[field]

        if "id_task" not in params or "cargo_name" not in params:
            return jsonify({"error": "Required fields: cargo_name, id_task"}), 400

        query = f"""
            INSERT INTO tbl_cargo ({', '.join(insert_fields)})
            VALUES ({', '.join(insert_values)})
            RETURNING cargo_id
        """

        result = current_session.execute(text(query), params)
        current_session.commit()

        cargo_id = result.fetchone()._mapping["cargo_id"]

        return jsonify({
            "message": "Cargo created successfully",
            "id": cargo_id,
            "name": data.get("cargo_name")
        }), 201

    except Exception as e:
        current_session.rollback()
        logger.error(f"Error creating cargo: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()