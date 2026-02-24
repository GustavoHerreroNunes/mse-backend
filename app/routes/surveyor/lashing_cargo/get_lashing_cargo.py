from flask import jsonify
from sqlalchemy import text

from app.services import Session
from . import lashing_cargo_bp, logger
from .schema import lashing_cargo_list_schema

@lashing_cargo_bp.route('/<int:cargo_id>', methods=['GET'])
def get_lashing_cargo(cargo_id):
    """Get all cargo info for a specific cargo"""
    current_session = Session()
    
    try:
        cargos = current_session.execute(
            text("SELECT * FROM tbl_step_lashing WHERE cargo_id = :cargo_id"),
            {"cargo_id": cargo_id}
        )
        
        return lashing_cargo_list_schema.dumps(cargos)
    except Exception as e:
        current_session.rollback()
        logger.error(f"Error retrieving lashing cargo: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()