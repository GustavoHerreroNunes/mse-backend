from flask import jsonify
from sqlalchemy import text

from app.services import Session
from . import cargo_condition_bp, logger
from .schema import cargo_condition_list_schema

@cargo_condition_bp.route('/<int:cargo_id>', methods=['GET'])
def get_cargo_condition(cargo_id):
    """Get all cargo condition info for a specific cargo"""
    current_session = Session()
    
    try:
        cargo = current_session.execute(
            text("SELECT * FROM tbl_cargo_condition WHERE cargo_id = :cargo_id"),
            {"cargo_id": cargo_id}
        )
        
        return cargo_condition_list_schema.dumps(cargo)
    except Exception as e:
        current_session.rollback()
        logger.error(f"Error retrieving cargo conditions: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()