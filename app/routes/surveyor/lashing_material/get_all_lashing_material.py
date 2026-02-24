from flask import jsonify, request
from sqlalchemy import text

from app.services import Session
from . import lashing_material_bp, logger
from .schema import lashing_material_list_schema

@lashing_material_bp.route('/all/<int:id_task>', methods=['GET'])
def get_all_lashing_material(id_task):
    """Get all lashing material info for a specific task"""
    current_session = Session()

    try:
        # pega id_cargo de query string
        id_cargo = request.args.get("id_cargo", type=int)

        cargos = current_session.execute(
            text("""
                SELECT 
                    lm.*,
                    EXISTS (
                        SELECT 1 
                        FROM rlt_lashing_cargo r
                        WHERE r.id_cargo = :id_cargo 
                        AND r.id_lashing_material = lm.id_lashing_material
                    ) AS has_relation,
                    EXISTS (
                        SELECT 1
                        FROM tbl_lashing_material m
                        WHERE m.id_lashing_material = lm.id_lashing_material
                        AND (
                            EXISTS (SELECT 1 FROM tbl_lashing_stopper    st WHERE st.id_lashing_material = lm.id_lashing_material)
                            OR EXISTS (SELECT 1 FROM tbl_lashing_wire       w  WHERE w.id_lashing_material = lm.id_lashing_material)
                            OR EXISTS (SELECT 1 FROM tbl_lashing_lines      l  WHERE l.id_lashing_material = lm.id_lashing_material)
                            OR EXISTS (SELECT 1 FROM tbl_lashing_shackles   sh WHERE sh.id_lashing_material = lm.id_lashing_material)
                            OR EXISTS (SELECT 1 FROM tbl_lashing_chain      c  WHERE c.id_lashing_material = lm.id_lashing_material)
                            OR EXISTS (SELECT 1 FROM tbl_lashing_tensioner  t  WHERE t.id_lashing_material = lm.id_lashing_material)
                        )
                    ) AS has_inspection
                FROM tbl_lashing_material lm
                WHERE lm.id_task = :id_task
            """),
            {"id_task": id_task, "id_cargo": id_cargo}
        )
        
        rows = cargos.mappings().all()  # converte para dict-like
        return jsonify(lashing_material_list_schema.dump(rows)), 200

    except Exception as e:
        current_session.rollback()
        logger.error(f"Error retrieving lashing material: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()
