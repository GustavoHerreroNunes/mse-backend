from flask import request, jsonify
from sqlalchemy import text
from app.services import Session
from . import cargo_storage_bp, logger
from .schema import cargo_storage_schema

@cargo_storage_bp.route('/', methods=['POST'])
def add_cargo_storage():
    """Add new cargo storage"""
    data = cargo_storage_schema.load(request.json)
    current_session = Session()
    
    try:
        # Verifica se o cargo existe na tabela tbl_cargo
        cargo_exists = current_session.execute(
            text("SELECT cargo_id FROM tbl_cargo WHERE cargo_id = :id"),
            {"id": data.get("cargo_id")}
        )

        if not list(cargo_exists):
            return jsonify({"error": "Cargo not found"}), 404

        # Verifica se o cargo_id já existe na tabela tbl_step_storage
        already_exists = current_session.execute(
            text("SELECT 1 FROM tbl_step_storage WHERE cargo_id = :id"),
            {"id": data.get("cargo_id")}
        )

        if already_exists.first():
            return jsonify({"error": "Cargo storage already exists"}), 409

        # Insere novo registro
        result = current_session.execute(
            text("INSERT INTO tbl_step_storage (cargo_id) VALUES (:id) RETURNING cargo_id"),
            {"id": data.get("cargo_id")}
        )

        current_session.commit()
        cargo_id = result.fetchone()._mapping["cargo_id"]

        return jsonify({
            "message": "Cargo storage created successfully", 
            "id": cargo_id
        }), 201

    except Exception as e:
        current_session.rollback()
        logger.error(f"Error creating cargo storage: {str(e)}")
        return jsonify({"error": str(e)}), 500

    finally:
        current_session.close()