from flask import jsonify
from sqlalchemy import text

from app.services import Session
from . import cargo_bp, logger
from .schema import cargo_list_schema

@cargo_bp.route('/by_task/<int:id_task>', methods=['GET'])
def get_cargo(id_task):
    """Get all cargo info for a specific cargo"""
    current_session = Session()
    
    try:
        cargo = current_session.execute(
            text("""SELECT 
                        tc.*,
                        EXISTS(
                            SELECT c.*
                            FROM tbl_cargo c
                            WHERE c.cargo_id = tc.cargo_id
                            AND (
                                EXISTS (SELECT 1 FROM tbl_cargo_condition_reel      cr WHERE cr.cargo_id = c.cargo_id)
                                OR EXISTS (SELECT 1 FROM tbl_cargo_condition_bale      cb WHERE cb.cargo_id = c.cargo_id)
                                OR EXISTS (SELECT 1 FROM tbl_cargo_condition_thd       ct WHERE ct.cargo_id = c.cargo_id)
                                OR EXISTS (SELECT 1 FROM tbl_cargo_condition_machinery cm WHERE cm.cargo_id = c.cargo_id)
                                OR EXISTS (SELECT 1 FROM tbl_cargo_condition_steel     cs WHERE cs.cargo_id = c.cargo_id)
                                OR EXISTS (SELECT 1 FROM tbl_cargo_condition_wood      cw WHERE cw.cargo_id = c.cargo_id)
                                OR EXISTS (SELECT 1 FROM tbl_cargo_condition_metallic  cm2 WHERE cm2.cargo_id = c.cargo_id)
                            )
                        ) AS has_inspection
                  FROM tbl_cargo tc WHERE tc.id_task = :id_task ORDER BY tc.cargo_id"""),
            {"id_task": id_task}
        )
        
        return cargo_list_schema.dumps(cargo)
    except Exception as e:
        current_session.rollback()
        logger.error(f"Error retrieving cargo: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()