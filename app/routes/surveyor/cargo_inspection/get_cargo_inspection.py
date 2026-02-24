from flask import jsonify
from sqlalchemy import text

from app.services import Session
from . import cargo_inspection_bp, logger
from .schema import (cargo_wood_list_schema, cargo_bale_list_schema, cargo_machinery_list_schema,
                    cargo_metallic_list_schema, cargo_reel_list_schema, cargo_steel_list_schema,
                    cargo_thd_list_schema
                    )

@cargo_inspection_bp.route('/<int:cargo_id>/<string:cargo_type>', methods=['GET'])
def get_cargo_inspection(cargo_id, cargo_type):
    """Get all cargo info for a specific cargo"""
    current_session = Session()
    
    try:
        if cargo_type == 'Wooden Crate':
            cargos = current_session.execute(
                text("SELECT * FROM tbl_cargo_condition_wood WHERE cargo_id = :cargo_id"),
                {"cargo_id": cargo_id}
            )
            return cargo_wood_list_schema.dumps(cargos)
        elif cargo_type == 'Steel Pipes':
            cargos = current_session.execute(
                text("SELECT * FROM tbl_cargo_condition_steel WHERE cargo_id = :cargo_id"),
                {"cargo_id": cargo_id}
            )
            return cargo_steel_list_schema.dumps(cargos)
        elif cargo_type == 'Machinery':
            cargos = current_session.execute(
                text("SELECT * FROM tbl_cargo_condition_machinery WHERE cargo_id = :cargo_id"),
                {"cargo_id": cargo_id}
            )
            return cargo_machinery_list_schema.dumps(cargos)
        elif cargo_type == 'Xtree or THD':
            cargos = current_session.execute(
                text("SELECT * FROM tbl_cargo_condition_thd WHERE cargo_id = :cargo_id"),
                {"cargo_id": cargo_id}
            )
            return cargo_thd_list_schema.dumps(cargos)
        elif cargo_type == 'Bale or Bagged':
            cargos = current_session.execute(
                text("SELECT * FROM tbl_cargo_condition_bale WHERE cargo_id = :cargo_id"),
                {"cargo_id": cargo_id}
            )
            return cargo_bale_list_schema.dumps(cargos)
        elif cargo_type == 'Metallic':
            cargos = current_session.execute(
                text("SELECT * FROM tbl_cargo_condition_metallic WHERE cargo_id = :cargo_id"),
                {"cargo_id": cargo_id}
            )
            return cargo_metallic_list_schema.dumps(cargos)
        elif cargo_type == 'Reel':
            cargos = current_session.execute(
                text("SELECT * FROM tbl_cargo_condition_reel WHERE cargo_id = :cargo_id"),
                {"cargo_id": cargo_id}
            )
            return cargo_reel_list_schema.dumps(cargos)
        else:
            return jsonify({"error": "Cargo type not found"}), 404

    except Exception as e:
        current_session.rollback()
        logger.error(f"Error retrieving cargo type {cargo_type}: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()