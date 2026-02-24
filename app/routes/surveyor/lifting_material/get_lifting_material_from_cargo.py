from flask import jsonify
from sqlalchemy import text

from app.services import Session
from . import lifting_material_bp, logger
from .schema import lifting_material_list_schema

@lifting_material_bp.route('/cargo/<int:id_cargo>', methods=['GET'])
def get_lifting_material_from_cargo(id_cargo):
    """Get lashing material info for a specific lifting material"""
    current_session = Session()
    
    try:
        cargos = current_session.execute(
            text("""
                    SELECT * FROM tbl_lifting_material tlm
                    left join rlt_lifting_cargo rlc on rlc.id_lifting_material = tlm.id_lifting_material
                    WHERE rlc.id_cargo = :id_cargo
                """),
            {"id_cargo": id_cargo}
        )
        
        return lifting_material_list_schema.dumps(cargos)
    except Exception as e:
        current_session.rollback()
        logger.error(f"Error retrieving lifting material: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()