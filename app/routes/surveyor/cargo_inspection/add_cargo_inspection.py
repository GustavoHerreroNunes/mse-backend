from flask import request, jsonify
from sqlalchemy import text
from app.services import Session
from . import cargo_inspection_bp, logger
from .schema import cargo_wood_schema

@cargo_inspection_bp.route('/<string:cargo_type>', methods=['POST'])
def add_cargo_inspection(cargo_type):
    """Add new cargo"""
    data = cargo_wood_schema.load(request.json)
    current_session = Session()
    
    try:
        # Verifica se o cargo existe na tabela tbl_cargo
        cargo_exists = current_session.execute(
            text("SELECT cargo_id FROM tbl_cargo WHERE cargo_id = :id"),
            {"id": data.get("cargo_id")}
        )

        if not list(cargo_exists):
            return jsonify({"error": "Cargo not found"}), 404

        if cargo_type == 'Wooden Crate':
            # Verifica se o cargo_id já existe na tabela tbl_cargo_condition_wood
            already_exists = current_session.execute(
                text("SELECT 1 FROM tbl_cargo_condition_wood WHERE cargo_id = :id"),
                {"id": data.get("cargo_id")}
            )

            if already_exists.first():
                return jsonify({"error": "Cargo inspection already exists"}), 409

            # Insere novo registro
            result = current_session.execute(
                text("INSERT INTO tbl_cargo_condition_wood (cargo_id) VALUES (:id) RETURNING cargo_id"),
                {"id": data.get("cargo_id")}
            )
        elif cargo_type == 'Steel Pipes':
            # Verifica se o cargo_id já existe na tabela tbl_cargo_condition_wood
            already_exists = current_session.execute(
                text("SELECT 1 FROM tbl_cargo_condition_steel WHERE cargo_id = :id"),
                {"id": data.get("cargo_id")}
            )

            if already_exists.first():
                return jsonify({"error": "Cargo inspection already exists"}), 409

            # Insere novo registro
            result = current_session.execute(
                text("INSERT INTO tbl_cargo_condition_steel (cargo_id) VALUES (:id) RETURNING cargo_id"),
                {"id": data.get("cargo_id")}
            )
        elif cargo_type == 'Machinery':
            # Verifica se o cargo_id já existe na tabela tbl_cargo_condition_wood
            already_exists = current_session.execute(
                text("SELECT 1 FROM tbl_cargo_condition_machinery WHERE cargo_id = :id"),
                {"id": data.get("cargo_id")}
            )

            if already_exists.first():
                return jsonify({"error": "Cargo inspection already exists"}), 409

            # Insere novo registro
            result = current_session.execute(
                text("INSERT INTO tbl_cargo_condition_machinery (cargo_id) VALUES (:id) RETURNING cargo_id"),
                {"id": data.get("cargo_id")}
            )
        elif cargo_type == 'Xtree or THD':
            # Verifica se o cargo_id já existe na tabela tbl_cargo_condition_wood
            already_exists = current_session.execute(
                text("SELECT 1 FROM tbl_cargo_condition_thd WHERE cargo_id = :id"),
                {"id": data.get("cargo_id")}
            )

            if already_exists.first():
                return jsonify({"error": "Cargo inspection already exists"}), 409

            # Insere novo registro
            result = current_session.execute(
                text("INSERT INTO tbl_cargo_condition_thd (cargo_id) VALUES (:id) RETURNING cargo_id"),
                {"id": data.get("cargo_id")}
            )
        elif cargo_type == 'Bale or Bagged':
            # Verifica se o cargo_id já existe na tabela tbl_cargo_condition_wood
            already_exists = current_session.execute(
                text("SELECT 1 FROM tbl_cargo_condition_bale WHERE cargo_id = :id"),
                {"id": data.get("cargo_id")}
            )

            if already_exists.first():
                return jsonify({"error": "Cargo inspection already exists"}), 409

            # Insere novo registro
            result = current_session.execute(
                text("INSERT INTO tbl_cargo_condition_bale (cargo_id) VALUES (:id) RETURNING cargo_id"),
                {"id": data.get("cargo_id")}
            )
        elif cargo_type == 'Metallic':
            # Verifica se o cargo_id já existe na tabela tbl_cargo_condition_wood
            already_exists = current_session.execute(
                text("SELECT 1 FROM tbl_cargo_condition_metallic WHERE cargo_id = :id"),
                {"id": data.get("cargo_id")}
            )

            if already_exists.first():
                return jsonify({"error": "Cargo inspection already exists"}), 409

            # Insere novo registro
            result = current_session.execute(
                text("INSERT INTO tbl_cargo_condition_metallic (cargo_id) VALUES (:id) RETURNING cargo_id"),
                {"id": data.get("cargo_id")}
            )
        elif cargo_type == 'Reel':
            # Verifica se o cargo_id já existe na tabela tbl_cargo_condition_wood
            already_exists = current_session.execute(
                text("SELECT 1 FROM tbl_cargo_condition_reel WHERE cargo_id = :id"),
                {"id": data.get("cargo_id")}
            )

            if already_exists.first():
                return jsonify({"error": "Cargo inspection already exists"}), 409

            # Insere novo registro
            result = current_session.execute(
                text("INSERT INTO tbl_cargo_condition_reel (cargo_id) VALUES (:id) RETURNING cargo_id"),
                {"id": data.get("cargo_id")}
            )
        else:
            return jsonify({"error": "Cargo type not found"}), 404
        
        current_session.commit()
        cargo_id = result.fetchone()._mapping["cargo_id"]

        return jsonify({
            "message": "Cargo inspection created successfully", 
            "id": cargo_id
        }), 201

    except Exception as e:
        current_session.rollback()
        logger.error(f"Error creating cargo inspection: {str(e)}")
        return jsonify({"error": str(e)}), 500

    finally:
        current_session.close()