from flask import jsonify, request
from sqlalchemy import text
from marshmallow import ValidationError

from app.services import Session
from . import tasks_survey_bp, logger
from ..tasks_survey.schema import task_survey_list_schema
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@tasks_survey_bp.route('/boarding/task/<int:task_id>', methods=['GET'])
def get_all_info_task(task_id):
    """Get all information for a specific task"""
    current_session = Session()

    try:
        # Buscar todos os campos necessários para o schema
        task_result = current_session.execute(
            text("SELECT * FROM tbl_task_survey_boarding WHERE id_task = :id"),
            {"id": task_id}
        )

        # Use `.mappings().all()` para garantir que o resultado seja uma lista de dicionários
        rows = task_result.mappings().all()

        if not rows:
            return jsonify({"error": "Task not found"}), 404

        # rows já é uma lista de dicionários, não precisa de conversão
        return jsonify(task_survey_list_schema.dump(rows)), 200

    except Exception as e:
        current_session.rollback()
        logger.error(f"Error retrieving task: {str(e)}")
        return jsonify({"error": str(e)}), 500

    finally:
        current_session.close() 