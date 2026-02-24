from flask import jsonify, request
from marshmallow import ValidationError
from app.services import Session
from sqlalchemy import text
from .schema import task_survey_schema
from . import tasks_survey_bp

@tasks_survey_bp.route('/boarding/internal/<int:task_id>', methods=['PUT'])
def update_internal_areas(task_id):
    """
    Update the fields `storage_adequate` from a boarding task.
    Note: The `id_survey` value cannot be changed.
    """
    try:
        data = task_survey_schema.load(request.json, partial=True)

        if not data:
            return jsonify({"error": "No update data provided"}), 400

        if "storage_adequate" not in data:
            return jsonify({"error": "The field storage_adequate is required for update"}), 400

        current_session = Session()
        try:
            task_query = current_session.execute(
                text("SELECT * FROM tbl_task_survey_boarding WHERE id_task = :id"),
                {"id": task_id}
            )

            if not list(task_query):
                return jsonify({"error": "Boarding task not found"}), 404

            update_fields = []
            params = {"id": task_id}

            for field, value in data.items():
                update_fields.append(f"{field} = :{field}")
                params[field] = value

            update_query = f"""
                UPDATE tbl_task_survey_boarding 
                SET {', '.join(update_fields)}
                WHERE id_task = :id
            """

            current_session.execute(text(update_query), params)
            current_session.commit()

            return jsonify({"message": "Boarding task updated successfully"}), 200

        except Exception as e:
            current_session.rollback()
            return jsonify({"error": str(e)}), 500

        finally:
            current_session.close()

    except ValidationError as e:
        return jsonify({"error": "Validation Error.", "details": e.messages}), 400