from flask import jsonify
from sqlalchemy import text

from app.services import Session
from . import lashing_inspection_bp

@lashing_inspection_bp.route('/<int:lashing_id>/<string:lashing_type>', methods=['DELETE'])
def delete_lashing_inspection(lashing_id, lashing_type):
    """Delete lashing inspection by id"""
    current_session = Session()
    
    try:

        if lashing_type == 'Wire Ropes':
            lashing = current_session.execute(
                text("SELECT id_lashing_material FROM tbl_lashing_wire WHERE id_lashing_material = :id"),
                {"id": lashing_id}
            )
            
            if not list(lashing):
                return jsonify({"error": "Lashing not found"}), 404
            
            current_session.execute(
                text("DELETE FROM tbl_lashing_wire WHERE id_lashing_material = :id"),
                {"id": lashing_id}
            )
        elif lashing_type == 'Synthetic Lines':
            lashing = current_session.execute(
                text("SELECT id_lashing_material FROM tbl_lashing_lines WHERE id_lashing_material = :id"),
                {"id": lashing_id}
            )
            
            if not list(lashing):
                return jsonify({"error": "Lashing not found"}), 404
            
            current_session.execute(
                text("DELETE FROM tbl_lashing_lines WHERE id_lashing_material = :id"),
                {"id": lashing_id}
            )
        elif lashing_type == 'Shackles':
            lashing = current_session.execute(
                text("SELECT id_lashing_material FROM tbl_lashing_shackles WHERE id_lashing_material = :id"),
                {"id": lashing_id}
            )
            
            if not list(lashing):
                return jsonify({"error": "Lashing not found"}), 404
            
            current_session.execute(
                text("DELETE FROM tbl_lashing_shackles WHERE id_lashing_material = :id"),
                {"id": lashing_id}
            )
        elif lashing_type == 'Chain':
            lashing = current_session.execute(
                text("SELECT id_lashing_material FROM tbl_lashing_chain WHERE id_lashing_material = :id"),
                {"id": lashing_id}
            )
            
            if not list(lashing):
                return jsonify({"error": "Lashing not found"}), 404
            
            current_session.execute(
                text("DELETE FROM tbl_lashing_chain WHERE id_lashing_material = :id"),
                {"id": lashing_id}
            )
        elif lashing_type == 'Stopper, dog plate':
            lashing = current_session.execute(
                text("SELECT id_lashing_material FROM tbl_lashing_stopper WHERE id_lashing_material = :id"),
                {"id": lashing_id}
            )
            
            if not list(lashing):
                return jsonify({"error": "Lashing not found"}), 404
            
            current_session.execute(
                text("DELETE FROM tbl_lashing_stopper WHERE id_lashing_material = :id"),
                {"id": lashing_id}
            )
        elif lashing_type == 'Tensioner, turnbuckle, arm lever':
            lashing = current_session.execute(
                text("SELECT id_lashing_material FROM tbl_lashing_tensioner WHERE id_lashing_material = :id"),
                {"id": lashing_id}
            )
            
            if not list(lashing):
                return jsonify({"error": "Lashing not found"}), 404
            
            current_session.execute(
                text("DELETE FROM tbl_lashing_tensioner WHERE id_lashing_material = :id"),
                {"id": lashing_id}
            )
        else:
            return jsonify({"error": "Lashing type not found"}), 404
        
        current_session.commit()
        
        return jsonify({"message": "Lashing inspection deleted successfully"}), 200
    except Exception as e:
        current_session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()