from flask import jsonify
from sqlalchemy import text

from app.services import Session
from . import lifting_material_bp

@lifting_material_bp.route('/<int:id_lifting_material>', methods=['DELETE'])
def delete_lifting_material(id_lifting_material):
    """Delete lifting material by id"""
    current_session = Session()
    
    try:
        # Check if lifting material exists
        cargo = current_session.execute(
            text("SELECT id_lifting_material FROM tbl_lifting_material WHERE id_lifting_material = :id"),
            {"id": id_lifting_material}
        )
        
        if not list(cargo):
            return jsonify({"error": "Lifting material not found"}), 404
        
        current_session.execute(
            text("DELETE FROM tbl_lifting_material WHERE id_lifting_material = :id"),
            {"id": id_lifting_material}
        )
        
        current_session.commit()
        
        return jsonify({"message": "Lifting material deleted successfully"}), 200
    except Exception as e:
        current_session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()