from flask import jsonify
from sqlalchemy import text

from app.services import Session
from . import lashing_material_bp, logger
from .schema import lashing_material_list_schema

@lashing_material_bp.route('/cargo/<int:id_cargo>', methods=['GET'])
def get_lashing_material_from_cargo(id_cargo):
    """Get all lashing material info for a specific task"""
    current_session = Session()
    
    try:
        cargos = current_session.execute(
            text("""
                    SELECT * FROM tbl_lashing_material tlm
                    left join rlt_lashing_cargo rlc on rlc.id_lashing_material = tlm.id_lashing_material
                    WHERE rlc.id_cargo = :id_cargo
                """),
            {"id_cargo": id_cargo}
        )
        
        return lashing_material_list_schema.dumps(cargos)
    except Exception as e:
        current_session.rollback()
        logger.error(f"Error retrieving lashing material: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()