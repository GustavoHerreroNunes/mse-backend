from flask import jsonify
from sqlalchemy import text

from app.services import Session
from . import cargo_bp

@cargo_bp.route('/<int:cargo_id>', methods=['DELETE'])
def delete_cargo(cargo_id):
    """Delete cargo by id"""
    current_session = Session()
    
    try:
        # Check if notification exists
        cargo = current_session.execute(
            text("SELECT cargo_id FROM tbl_cargo WHERE cargo_id = :id"),
            {"id": cargo_id}
        )
        
        if not list(cargo):
            return jsonify({"error": "Cargo not found"}), 404
        
        current_session.execute(
            text("DELETE FROM tbl_cargo WHERE cargo_id = :id"),
            {"id": cargo_id}
        )
        
        current_session.commit()
        
        return jsonify({"message": "Cargo deleted successfully"}), 200
    except Exception as e:
        current_session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()