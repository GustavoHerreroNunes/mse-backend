from flask import jsonify
from sqlalchemy import text

from app.services import Session
from . import lifting_material_bp, logger
from .schema import lifting_material_list_schema

@lifting_material_bp.route('/<int:id_lifting_material>', methods=['GET'])
def get_lifting_material(id_lifting_material):
    """Get lashing material info for a specific lifting material"""
    current_session = Session()
    
    try:
        cargos = current_session.execute(
            text("SELECT * FROM tbl_lifting_material WHERE id_lifting_material = :id_lifting_material"),
            {"id_lifting_material": id_lifting_material}
        )
        
        return lifting_material_list_schema.dumps(cargos)
    except Exception as e:
        current_session.rollback()
        logger.error(f"Error retrieving lifting material: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()