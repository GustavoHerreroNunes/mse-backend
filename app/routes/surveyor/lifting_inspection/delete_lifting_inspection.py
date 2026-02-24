from flask import jsonify
from sqlalchemy import text

from app.services import Session
from . import lifting_inspection_bp

@lifting_inspection_bp.route('/<int:lifting_id>/<string:lifting_type>', methods=['DELETE'])
def delete_lifting_inspection(lifting_id, lifting_type):
    """Delete lifting inspection by id"""
    current_session = Session()
    
    try:

        if lifting_type == 'Wire Ropes':
            lifting = current_session.execute(
                text("SELECT id_lifting_material FROM tbl_lifting_wire WHERE id_lifting_material = :id"),
                {"id": lifting_id}
            )
            
            if not list(lifting):
                return jsonify({"error": "Lifting not found"}), 404
            
            current_session.execute(
                text("DELETE FROM tbl_lifting_wire WHERE id_lifting_material = :id"),
                {"id": lifting_id}
            )
        elif lifting_type == 'Synthetic Sling':
            lifting = current_session.execute(
                text("SELECT id_lifting_material FROM tbl_lifting_sling WHERE id_lifting_material = :id"),
                {"id": lifting_id}
            )
            
            if not list(lifting):
                return jsonify({"error": "Lifting not found"}), 404
            
            current_session.execute(
                text("DELETE FROM tbl_lifting_sling WHERE id_lifting_material = :id"),
                {"id": lifting_id}
            )
        elif lifting_type == 'Shackles':
            lifting = current_session.execute(
                text("SELECT id_lifting_material FROM tbl_lifting_shackles WHERE id_lifting_material = :id"),
                {"id": lifting_id}
            )
            
            if not list(lifting):
                return jsonify({"error": "Lifting not found"}), 404
            
            current_session.execute(
                text("DELETE FROM tbl_lifting_shackles WHERE id_lifting_material = :id"),
                {"id": lifting_id}
            )
        elif lifting_type == 'Spreader':
            lifting = current_session.execute(
                text("SELECT id_lifting_material FROM tbl_lifting_spreader WHERE id_lifting_material = :id"),
                {"id": lifting_id}
            )
            
            if not list(lifting):
                return jsonify({"error": "Lifting not found"}), 404
            
            current_session.execute(
                text("DELETE FROM tbl_lifting_spreader WHERE id_lifting_material = :id"),
                {"id": lifting_id}
            )
        elif lifting_type == 'Chain':
            lifting = current_session.execute(
                text("SELECT id_lifting_material FROM tbl_lifting_chain WHERE id_lifting_material = :id"),
                {"id": lifting_id}
            )
            
            if not list(lifting):
                return jsonify({"error": "Lifting not found"}), 404
            
            current_session.execute(
                text("DELETE FROM tbl_lifting_chain WHERE id_lifting_material = :id"),
                {"id": lifting_id}
            )
        elif lifting_type == 'Hook':
            lifting = current_session.execute(
                text("SELECT id_lifting_material FROM tbl_lifting_hook WHERE id_lifting_material = :id"),
                {"id": lifting_id}
            )
            
            if not list(lifting):
                return jsonify({"error": "Lifting not found"}), 404
            
            current_session.execute(
                text("DELETE FROM tbl_lifting_hook WHERE id_lifting_material = :id"),
                {"id": lifting_id}
            )
        elif lifting_type == 'Master Link':
            lifting = current_session.execute(
                text("SELECT id_lifting_material FROM tbl_lifting_link WHERE id_lifting_material = :id"),
                {"id": lifting_id}
            )
            
            if not list(lifting):
                return jsonify({"error": "Lifting not found"}), 404
            
            current_session.execute(
                text("DELETE FROM tbl_lifting_link WHERE id_lifting_material = :id"),
                {"id": lifting_id}
            )
        else:
            return jsonify({"error": "Lifting type not found"}), 404
        
        current_session.commit()
        
        return jsonify({"message": "Lifting inspection deleted successfully"}), 200
    except Exception as e:
        current_session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()