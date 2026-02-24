from flask import jsonify
from sqlalchemy import text

from app.services import Session
from . import cargo_storage_bp, logger
from .schema import cargo_storage_list_schema

@cargo_storage_bp.route('/<int:cargo_id>', methods=['GET'])
def get_cargo_storage(cargo_id):
    """Get all cargo storage info for a specific cargo"""
    current_session = Session()
    
    try:
        cargos = current_session.execute(
            text("SELECT * FROM tbl_step_storage WHERE cargo_id = :cargo_id"),
            {"cargo_id": cargo_id}
        )
        
        return cargo_storage_list_schema.dumps(cargos)
    except Exception as e:
        current_session.rollback()
        logger.error(f"Error retrieving cargo storage: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()