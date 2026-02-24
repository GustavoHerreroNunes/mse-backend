from flask import jsonify
from sqlalchemy import text

from app.services import Session
from . import lashing_material_bp, logger
from .schema import lashing_material_list_schema

@lashing_material_bp.route('/<int:id_lashing_material>', methods=['GET'])
def get_lashing_material(id_lashing_material):
    """Get lashing material info for a specific lashing material"""
    current_session = Session()
    
    try:
        cargos = current_session.execute(
            text("SELECT * FROM tbl_lashing_material WHERE id_lashing_material = :id_lashing_material"),
            {"id_lashing_material": id_lashing_material}
        )
        
        return lashing_material_list_schema.dumps(cargos)
    except Exception as e:
        current_session.rollback()
        logger.error(f"Error retrieving lashing material: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()