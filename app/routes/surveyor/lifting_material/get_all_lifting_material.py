from flask import jsonify, request
from sqlalchemy import text

from app.services import Session
from . import lifting_material_bp, logger
from .schema import lifting_material_list_schema

@lifting_material_bp.route('/all/<int:id_task>', methods=['GET'])
def get_all_lifting_material(id_task):
    """Get all lifting material info for a specific task"""
    current_session = Session()

    try:
        id_cargo = request.args.get("id_cargo", type=int)

        cargos = current_session.execute(
            text("""
                SELECT 
                    lm.*,
                    EXISTS (
                        SELECT 1 
                        FROM rlt_lifting_cargo r
                        WHERE r.id_cargo = :id_cargo 
                        AND r.id_lifting_material = lm.id_lifting_material
                    ) AS has_relation,
                    EXISTS (
                        SELECT 1
                        FROM tbl_lifting_material m
                        WHERE m.id_lifting_material = lm.id_lifting_material
                        AND (
                            EXISTS (SELECT 1 FROM tbl_lifting_wire      w WHERE w.id_lifting_material = m.id_lifting_material)
                            OR EXISTS (SELECT 1 FROM tbl_lifting_sling     s WHERE s.id_lifting_material = m.id_lifting_material)
                            OR EXISTS (SELECT 1 FROM tbl_lifting_shackles  sh WHERE sh.id_lifting_material = m.id_lifting_material)
                            OR EXISTS (SELECT 1 FROM tbl_lifting_spreader  sp WHERE sp.id_lifting_material = m.id_lifting_material)
                            OR EXISTS (SELECT 1 FROM tbl_lifting_chain     c WHERE c.id_lifting_material = m.id_lifting_material)
                            OR EXISTS (SELECT 1 FROM tbl_lifting_hook      h WHERE h.id_lifting_material = m.id_lifting_material)
                            OR EXISTS (SELECT 1 FROM tbl_lifting_link      l WHERE l.id_lifting_material = m.id_lifting_material)
                        )
                    ) AS has_inspection
                FROM tbl_lifting_material lm
                WHERE lm.id_task = :id_task
            """),
            {"id_task": id_task, "id_cargo": id_cargo}
        )
        
        return lifting_material_list_schema.dumps(cargos)
    except Exception as e:
        current_session.rollback()
        logger.error(f"Error retrieving lifting material: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()