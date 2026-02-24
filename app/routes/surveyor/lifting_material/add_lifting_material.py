from flask import request, jsonify
from sqlalchemy import text
from app.services import Session
from . import lifting_material_bp, logger
from .schema import lifting_material_schema

@lifting_material_bp.route('/', methods=['POST'])
def add_lifting_material():
    """Add new lifting material"""
    data = lifting_material_schema.load(request.json)
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
            "id_task", 
            "type", 
            "quantity",
            "weight", 
            "lenght"
        ]

        insert_fields = []
        insert_values = []
        params = {}

        for field in fields_to_insert:
            if field in data:
                insert_fields.append(field)
                insert_values.append(f":{field}")
                params[field] = data[field]

        if "id_task" not in params or "type" not in params or "quantity" not in params or "weight" not in params:
            return jsonify({"error": "Required fields: id_task, type, quantity, weight"}), 400

        query = f"""
            INSERT INTO tbl_lifting_material ({', '.join(insert_fields)})
            VALUES ({', '.join(insert_values)})
            RETURNING id_lifting_material
        """

        result = current_session.execute(text(query), params)
        current_session.commit()

        id_lifting_material = result.fetchone()._mapping["id_lifting_material"]

        return jsonify({
            "message": "Lifting material created successfully",
            "id": id_lifting_material
        }), 201

    except Exception as e:
        current_session.rollback()
        logger.error(f"Error creating lashing material: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()