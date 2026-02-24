from flask import jsonify
from sqlalchemy import text

from app.services import Session
from . import lashing_inspection_bp, logger
from .schema import (lashing_chain_list_schema, lashing_shackles_list_schema, lashing_lines_list_schema,
                    lashing_wire_list_schema, lashing_stopper_list_schema, lashing_tensioner_list_schema
                    )

@lashing_inspection_bp.route('/<int:lashing_id>/<string:lashing_type>', methods=['GET'])
def get_lashing_inspection(lashing_id, lashing_type):
    """Get all lashing info for a specific lashing"""
    current_session = Session()
    
    try:
        if lashing_type == 'Wire Ropes':
            lashings = current_session.execute(
                text("SELECT * FROM tbl_lashing_wire WHERE id_lashing_material = :lashing_id"),
                {"lashing_id": lashing_id}
            )
            return lashing_wire_list_schema.dumps(lashings)
        elif lashing_type == 'Synthetic Lines':
            lashings = current_session.execute(
                text("SELECT * FROM tbl_lashing_lines WHERE id_lashing_material = :lashing_id"),
                {"lashing_id": lashing_id}
            )
            return lashing_lines_list_schema.dumps(lashings)
        elif lashing_type == 'Shackles':
            lashings = current_session.execute(
                text("SELECT * FROM tbl_lashing_shackles WHERE id_lashing_material = :lashing_id"),
                {"lashing_id": lashing_id}
            )
            return lashing_shackles_list_schema.dumps(lashings)
        elif lashing_type == 'Chain':
            lashings = current_session.execute(
                text("SELECT * FROM tbl_lashing_chain WHERE id_lashing_material = :lashing_id"),
                {"lashing_id": lashing_id}
            )
            return lashing_chain_list_schema.dumps(lashings)
        elif lashing_type == 'Stopper, dog plate':
            lashings = current_session.execute(
                text("SELECT * FROM tbl_lashing_stopper WHERE id_lashing_material = :lashing_id"),
                {"lashing_id": lashing_id}
            )
            return lashing_stopper_list_schema.dumps(lashings)
        elif lashing_type == 'Tensioner, turnbuckle, arm lever':
            lashings = current_session.execute(
                text("SELECT * FROM tbl_lashing_tensioner WHERE id_lashing_material = :lashing_id"),
                {"lashing_id": lashing_id}
            )
            return lashing_tensioner_list_schema.dumps(lashings)
        else:
            return jsonify({"error": "Lashing type not found"}), 404

    except Exception as e:
        current_session.rollback()
        logger.error(f"Error retrieving lashing type {lashing_type}: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()