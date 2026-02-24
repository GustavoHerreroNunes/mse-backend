from flask import request, jsonify
from sqlalchemy import text
from app.services import Session
from . import survey_pdf_bp, logger
from .schema import survey_pdf_schema

@survey_pdf_bp.route('/', methods=['POST'])
def add_survey_pdf():
    """Add new preliminary checklist"""
    data = survey_pdf_schema.load(request.json)
    current_session = Session()
    
    try:
        # Verifica se a demanda existe na tabela tbl_demandas
        demanda_exists = current_session.execute(
            text("SELECT id_demanda FROM tbl_demandas WHERE id_demanda = :id"),
            {"id": data.get("id_demanda")}
        )

        if not list(demanda_exists):
            return jsonify({"error": "Demanda not found"}), 404

        # Verifica se o id_demanda já existe na tabela tbl_status_pdf
        already_exists = current_session.execute(
            text("SELECT 1 FROM tbl_status_pdf WHERE id_demanda = :id"),
            {"id": data.get("id_demanda")}
        )

        if already_exists.first():
            return jsonify({"error": "PDF status already exists"}), 409

        # Insere novo registro
        result = current_session.execute(
            text("INSERT INTO tbl_status_pdf (id_demanda) VALUES (:id) RETURNING id_demanda"),
            {"id": data.get("id_demanda")}
        )

        current_session.commit()
        id_demanda = result.fetchone()._mapping["id_demanda"]

        return jsonify({
            "message": "Status PDF created successfully", 
            "id": id_demanda
        }), 201

    except Exception as e:
        current_session.rollback()
        logger.error(f"Error creating status PDF: {str(e)}")
        return jsonify({"error": str(e)}), 500

    finally:
        current_session.close()
