from flask import jsonify
from sqlalchemy import text

from app.services import Session
from . import lashing_material_bp

@lashing_material_bp.route('/<int:id_lashing_material>', methods=['DELETE'])
def delete_lashing_material(id_lashing_material):
    """Delete lashing material by id"""
    current_session = Session()
    
    try:
        # Check if notification exists
        cargo = current_session.execute(
            text("SELECT id_lashing_material FROM tbl_lashing_material WHERE id_lashing_material = :id"),
            {"id": id_lashing_material}
        )
        
        if not list(cargo):
            return jsonify({"error": "Lashing material not found"}), 404
        
        current_session.execute(
            text("DELETE FROM tbl_lashing_material WHERE id_lashing_material = :id"),
            {"id": id_lashing_material}
        )
        
        current_session.commit()
        
        return jsonify({"message": "Lashing material deleted successfully"}), 200
    except Exception as e:
        current_session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()