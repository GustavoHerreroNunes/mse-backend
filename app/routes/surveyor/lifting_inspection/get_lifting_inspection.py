from flask import jsonify
from sqlalchemy import text

from app.services import Session
from . import lifting_inspection_bp, logger
from .schema import (lifting_chain_list_schema, lifting_hook_list_schema, lifting_link_list_schema,
                    lifting_shackles_list_schema, lifting_sling_list_schema, lifting_spreader_list_schema,
                    lifting_wire_list_schema
                    )

@lifting_inspection_bp.route('/<int:lifting_id>/<string:lifting_type>', methods=['GET'])
def get_lifting_inspection(lifting_id, lifting_type):
    """Get all lifting info for a specific lifting"""
    current_session = Session()
    
    try:
        if lifting_type == 'Wire Ropes':
            liftings = current_session.execute(
                text("SELECT * FROM tbl_lifting_wire WHERE id_lifting_material = :lifting_id"),
                {"lifting_id": lifting_id}
            )
            return lifting_wire_list_schema.dumps(liftings)
        elif lifting_type == 'Synthetic Sling':
            liftings = current_session.execute(
                text("SELECT * FROM tbl_lifting_sling WHERE id_lifting_material = :lifting_id"),
                {"lifting_id": lifting_id}
            )
            return lifting_sling_list_schema.dumps(liftings)
        elif lifting_type == 'Shackles':
            liftings = current_session.execute(
                text("SELECT * FROM tbl_lifting_shackles WHERE id_lifting_material = :lifting_id"),
                {"lifting_id": lifting_id}
            )
            return lifting_shackles_list_schema.dumps(liftings)
        elif lifting_type == 'Spreader':
            liftings = current_session.execute(
                text("SELECT * FROM tbl_lifting_spreader WHERE id_lifting_material = :lifting_id"),
                {"lifting_id": lifting_id}
            )
            return lifting_spreader_list_schema.dumps(liftings)
        elif lifting_type == 'Chain':
            liftings = current_session.execute(
                text("SELECT * FROM tbl_lifting_chain WHERE id_lifting_material = :lifting_id"),
                {"lifting_id": lifting_id}
            )
            return lifting_chain_list_schema.dumps(liftings)
        elif lifting_type == 'Hook':
            liftings = current_session.execute(
                text("SELECT * FROM tbl_lifting_hook WHERE id_lifting_material = :lifting_id"),
                {"lifting_id": lifting_id}
            )
            return lifting_hook_list_schema.dumps(liftings)
        elif lifting_type == 'Master Link':
            liftings = current_session.execute(
                text("SELECT * FROM tbl_lifting_link WHERE id_lifting_material = :lifting_id"),
                {"lifting_id": lifting_id}
            )
            return lifting_link_list_schema.dumps(liftings)
        else:
            return jsonify({"error": "Lifting type not found"}), 404

    except Exception as e:
        current_session.rollback()
        logger.error(f"Error retrieving lifting type {lifting_type}: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()