from flask import request, jsonify
from sqlalchemy import text
from app.services import Session
from . import lashing_inspection_bp, logger
from .schema import lashing_chain_schema

@lashing_inspection_bp.route('/<string:lashing_type>', methods=['POST'])
def add_lashing_inspection(lashing_type):
    """Add new lashing"""
    data = lashing_chain_schema.load(request.json)
    current_session = Session()
    
    try:
        # Verifica se o lashing material existe
        task_result = current_session.execute(
            text("SELECT id_lashing_material FROM tbl_lashing_material WHERE id_lashing_material = :id"),
            {"id": data.get("id_lashing_material")}
        )

        if not list(task_result):
            return jsonify({"error": "Lashing material not found"}), 404

        if lashing_type == 'Wire Ropes':
            # Verifica se o id_lashing_material já existe na tabela tbl_cargo_condition_wood
            already_exists = current_session.execute(
                text("SELECT 1 FROM tbl_lashing_wire WHERE id_lashing_material = :id"),
                {"id": data.get("id_lashing_material")}
            )

            if already_exists.first():
                return jsonify({"error": "Lashing material already exists"}), 409

            # Insere novo registro
            result = current_session.execute(
                text("INSERT INTO tbl_lashing_wire (id_lashing_material) VALUES (:id) RETURNING id_lashing_material"),
                {"id": data.get("id_lashing_material")}
            )
        elif lashing_type == 'Synthetic Lines':
            # Verifica se o id_lashing_material já existe na tabela tbl_cargo_condition_wood
            already_exists = current_session.execute(
                text("SELECT 1 FROM tbl_lashing_lines WHERE id_lashing_material = :id"),
                {"id": data.get("id_lashing_material")}
            )

            if already_exists.first():
                return jsonify({"error": "Lashing material already exists"}), 409

            # Insere novo registro
            result = current_session.execute(
                text("INSERT INTO tbl_lashing_lines (id_lashing_material) VALUES (:id) RETURNING id_lashing_material"),
                {"id": data.get("id_lashing_material")}
            )
        elif lashing_type == 'Shackles':
            # Verifica se o id_lashing_material já existe na tabela tbl_cargo_condition_wood
            already_exists = current_session.execute(
                text("SELECT 1 FROM tbl_lashing_shackles WHERE id_lashing_material = :id"),
                {"id": data.get("id_lashing_material")}
            )

            if already_exists.first():
                return jsonify({"error": "Lashing material already exists"}), 409

            # Insere novo registro
            result = current_session.execute(
                text("INSERT INTO tbl_lashing_shackles (id_lashing_material) VALUES (:id) RETURNING id_lashing_material"),
                {"id": data.get("id_lashing_material")}
            )
        elif lashing_type == 'Chain':
            # Verifica se o id_lashing_material já existe na tabela tbl_cargo_condition_wood
            already_exists = current_session.execute(
                text("SELECT 1 FROM tbl_lashing_chain WHERE id_lashing_material = :id"),
                {"id": data.get("id_lashing_material")}
            )

            if already_exists.first():
                return jsonify({"error": "Lashing material already exists"}), 409

            # Insere novo registro
            result = current_session.execute(
                text("INSERT INTO tbl_lashing_chain (id_lashing_material) VALUES (:id) RETURNING id_lashing_material"),
                {"id": data.get("id_lashing_material")}
            )
        elif lashing_type == 'Stopper, dog plate':
            # Verifica se o id_lashing_material já existe na tabela tbl_cargo_condition_wood
            already_exists = current_session.execute(
                text("SELECT 1 FROM tbl_lashing_stopper WHERE id_lashing_material = :id"),
                {"id": data.get("id_lashing_material")}
            )

            if already_exists.first():
                return jsonify({"error": "Lashing material already exists"}), 409

            # Insere novo registro
            result = current_session.execute(
                text("INSERT INTO tbl_lashing_stopper (id_lashing_material) VALUES (:id) RETURNING id_lashing_material"),
                {"id": data.get("id_lashing_material")}
            )
        elif lashing_type == 'Tensioner, turnbuckle, arm lever':
            # Verifica se o id_lashing_material já existe na tabela tbl_cargo_condition_wood
            already_exists = current_session.execute(
                text("SELECT 1 FROM tbl_lashing_tensioner WHERE id_lashing_material = :id"),
                {"id": data.get("id_lashing_material")}
            )

            if already_exists.first():
                return jsonify({"error": "Lashing material already exists"}), 409

            # Insere novo registro
            result = current_session.execute(
                text("INSERT INTO tbl_lashing_tensioner (id_lashing_material) VALUES (:id) RETURNING id_lashing_material"),
                {"id": data.get("id_lashing_material")}
            )
        else:
            return jsonify({"error": "Lashing type not found"}), 404
        
        current_session.commit()
        id_lashing_material = result.fetchone()._mapping["id_lashing_material"]

        return jsonify({
            "message": "Lashing material created successfully", 
            "id": id_lashing_material
        }), 201

    except Exception as e:
        current_session.rollback()
        logger.error(f"Error creating lashing inspection: {str(e)}")
        return jsonify({"error": str(e)}), 500

    finally:
        current_session.close()