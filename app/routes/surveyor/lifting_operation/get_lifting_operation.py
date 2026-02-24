from flask import jsonify
from sqlalchemy import text

from app.services import Session
from . import lifting_operation_bp, logger
from .schema import lifting_operation_list_schema

@lifting_operation_bp.route('/<int:cargo_id>', methods=['GET'])
def get_lifting_operation(cargo_id):
    """Get all lifting operation info for a specific cargo"""
    current_session = Session()
    
    try:
        cargos = current_session.execute(
            text("SELECT * FROM tbl_step_rigging WHERE cargo_id = :cargo_id"),
            {"cargo_id": cargo_id}
        )
        
        return lifting_operation_list_schema.dumps(cargos)
    except Exception as e:
        current_session.rollback()
        logger.error(f"Error retrieving cargo type wood: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()