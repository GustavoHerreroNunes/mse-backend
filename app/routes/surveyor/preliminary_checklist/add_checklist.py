from flask import request, jsonify
from sqlalchemy import text
from app.services import Session
from . import checklist_bp, logger
from .schema import checklist_schema

@checklist_bp.route('/', methods=['POST'])
def add_checklist():
    """Add new preliminary checklist"""
    data = checklist_schema.load(request.json)
    current_session = Session()
    
    try:
        # Verifica se o survey existe na tabela tbl_task_survey_boarding
        survey_exists = current_session.execute(
            text("SELECT id_survey FROM tbl_task_survey_boarding WHERE id_survey = :id"),
            {"id": data.get("id_survey")}
        )

        if not list(survey_exists):
            return jsonify({"error": "Survey not found"}), 404

        # Verifica se o cargo_id já existe na tabela tbl_preliminary_checklist
        already_exists = current_session.execute(
            text("SELECT 1 FROM tbl_preliminary_checklist WHERE id_survey = :id"),
            {"id": data.get("id_survey")}
        )

        if already_exists.first():
            return jsonify({"error": "Preliminary checklist already exists"}), 409

        # Insere novo registro
        result = current_session.execute(
            text("INSERT INTO tbl_preliminary_checklist (id_survey) VALUES (:id) RETURNING id_survey"),
            {"id": data.get("id_survey")}
        )

        current_session.commit()
        id_survey = result.fetchone()._mapping["id_survey"]

        return jsonify({
            "message": "Preliminary checklist created successfully", 
            "id": id_survey
        }), 201

    except Exception as e:
        current_session.rollback()
        logger.error(f"Error creating preliminary checklist: {str(e)}")
        return jsonify({"error": str(e)}), 500

    finally:
        current_session.close()
