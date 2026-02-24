from flask import jsonify
from sqlalchemy import text

from app.services import Session
from . import cargo_inspection_bp

@cargo_inspection_bp.route('/<int:cargo_id>/<string:cargo_type>', methods=['DELETE'])
def delete_cargo_inspection(cargo_id, cargo_type):
    """Delete cargo inspection by id"""
    current_session = Session()
    
    try:

        if cargo_type == 'Wooden Crate':
            cargo = current_session.execute(
                text("SELECT cargo_id FROM tbl_cargo_condition_wood WHERE cargo_id = :id"),
                {"id": cargo_id}
            )
            
            if not list(cargo):
                return jsonify({"error": "Cargo not found"}), 404
            
            current_session.execute(
                text("DELETE FROM tbl_cargo_condition_wood WHERE cargo_id = :id"),
                {"id": cargo_id}
            )
        elif cargo_type == 'Steel Pipes':
            cargo = current_session.execute(
                text("SELECT cargo_id FROM tbl_cargo_condition_steel WHERE cargo_id = :id"),
                {"id": cargo_id}
            )
            
            if not list(cargo):
                return jsonify({"error": "Cargo not found"}), 404
            
            current_session.execute(
                text("DELETE FROM tbl_cargo_condition_steel WHERE cargo_id = :id"),
                {"id": cargo_id}
            )
        elif cargo_type == 'Machinery':
            cargo = current_session.execute(
                text("SELECT cargo_id FROM tbl_cargo_condition_machinery WHERE cargo_id = :id"),
                {"id": cargo_id}
            )
            
            if not list(cargo):
                return jsonify({"error": "Cargo not found"}), 404
            
            current_session.execute(
                text("DELETE FROM tbl_cargo_condition_machinery WHERE cargo_id = :id"),
                {"id": cargo_id}
            )
        elif cargo_type == 'Xtree or THD':
            cargo = current_session.execute(
                text("SELECT cargo_id FROM tbl_cargo_condition_thd WHERE cargo_id = :id"),
                {"id": cargo_id}
            )
            
            if not list(cargo):
                return jsonify({"error": "Cargo not found"}), 404
            
            current_session.execute(
                text("DELETE FROM tbl_cargo_condition_thd WHERE cargo_id = :id"),
                {"id": cargo_id}
            )
        elif cargo_type == 'Bale or Bagged':
            cargo = current_session.execute(
                text("SELECT cargo_id FROM tbl_cargo_condition_bale WHERE cargo_id = :id"),
                {"id": cargo_id}
            )
            
            if not list(cargo):
                return jsonify({"error": "Cargo not found"}), 404
            
            current_session.execute(
                text("DELETE FROM tbl_cargo_condition_bale WHERE cargo_id = :id"),
                {"id": cargo_id}
            )
        elif cargo_type == 'Metallic':
            cargo = current_session.execute(
                text("SELECT cargo_id FROM tbl_cargo_condition_metallic WHERE cargo_id = :id"),
                {"id": cargo_id}
            )
            
            if not list(cargo):
                return jsonify({"error": "Cargo not found"}), 404
            
            current_session.execute(
                text("DELETE FROM tbl_cargo_condition_metallic WHERE cargo_id = :id"),
                {"id": cargo_id}
            )
        elif cargo_type == 'Reel':
            cargo = current_session.execute(
                text("SELECT cargo_id FROM tbl_cargo_condition_reel WHERE cargo_id = :id"),
                {"id": cargo_id}
            )
            
            if not list(cargo):
                return jsonify({"error": "Cargo not found"}), 404
            
            current_session.execute(
                text("DELETE FROM tbl_cargo_condition_reel WHERE cargo_id = :id"),
                {"id": cargo_id}
            )
        else:
            return jsonify({"error": "Cargo type not found"}), 404
        
        current_session.commit()
        
        return jsonify({"message": "Cargo inspection deleted successfully"}), 200
    except Exception as e:
        current_session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()