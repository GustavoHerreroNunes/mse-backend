from flask import request, jsonify
from sqlalchemy import text
from app.services import Session
from . import cargo_condition_bp, logger
from .schema import cargo_condition_schema

@cargo_condition_bp.route('/', methods=['POST'])
def add_cargo_condition():
    """Add new cargo condition"""
    data = cargo_condition_schema.load(request.json)
    current_session = Session()
    
    try:
        existing = current_session.execute(
            text("SELECT cargo_id FROM tbl_cargo_condition WHERE cargo_id = :id"),
            {"id": data.get("cargo_id")}
        )

        if list(existing):
            return jsonify({"error": "A cargo condition with this id already exists"}), 409
        
        not_existing = current_session.execute(
            text("SELECT cargo_id FROM tbl_cargo WHERE cargo_id = :id"),
            {"id": data.get("cargo_id")}
        )

        if not list(not_existing):
            return jsonify({"error": "Cargo not found"}), 404
        
        result = current_session.execute(
            text("INSERT INTO tbl_cargo_condition (cargo_id) VALUES (:id) RETURNING cargo_id"),
            {
                "id": data.get("cargo_id")
            }
        )

        current_session.commit()
        cargo_id = result.fetchone()._mapping["cargo_id"]

        return jsonify({
            "message": "Cargo condition created successfully", 
            "id": cargo_id
        }), 201
    except Exception as e:
        current_session.rollback()
        logger.error(f"Error creating cargo condition: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()