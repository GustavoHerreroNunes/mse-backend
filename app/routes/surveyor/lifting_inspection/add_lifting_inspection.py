from flask import request, jsonify
from sqlalchemy import text
from app.services import Session
from . import lifting_inspection_bp, logger
from .schema import lifting_chain_schema

@lifting_inspection_bp.route('/<string:lifting_type>', methods=['POST'])
def add_lifting_inspection(lifting_type):
    """Add new lifting"""
    data = lifting_chain_schema.load(request.json)
    current_session = Session()
    
    try:
        # Verifica se o lifting material existe
        task_result = current_session.execute(
            text("SELECT id_lifting_material FROM tbl_lifting_material WHERE id_lifting_material = :id"),
            {"id": data.get("id_lifting_material")}
        )

        if not list(task_result):
            return jsonify({"error": "Lifting material not found"}), 404

        if lifting_type == 'Wire Ropes':
            # Verifica se o id_lifting_material já existe na tabela tbl_cargo_condition_wood
            already_exists = current_session.execute(
                text("SELECT 1 FROM tbl_lifting_wire WHERE id_lifting_material = :id"),
                {"id": data.get("id_lifting_material")}
            )

            if already_exists.first():
                return jsonify({"error": "Lifting material already exists"}), 409

            # Insere novo registro
            result = current_session.execute(
                text("INSERT INTO tbl_lifting_wire (id_lifting_material) VALUES (:id) RETURNING id_lifting_material"),
                {"id": data.get("id_lifting_material")}
            )
        elif lifting_type == 'Synthetic Sling':
            # Verifica se o id_lifting_material já existe na tabela tbl_cargo_condition_wood
            already_exists = current_session.execute(
                text("SELECT 1 FROM tbl_lifting_sling WHERE id_lifting_material = :id"),
                {"id": data.get("id_lifting_material")}
            )

            if already_exists.first():
                return jsonify({"error": "Lifting material already exists"}), 409

            # Insere novo registro
            result = current_session.execute(
                text("INSERT INTO tbl_lifting_sling (id_lifting_material) VALUES (:id) RETURNING id_lifting_material"),
                {"id": data.get("id_lifting_material")}
            )
        elif lifting_type == 'Shackles':
            # Verifica se o id_lifting_material já existe na tabela tbl_cargo_condition_wood
            already_exists = current_session.execute(
                text("SELECT 1 FROM tbl_lifting_shackles WHERE id_lifting_material = :id"),
                {"id": data.get("id_lifting_material")}
            )

            if already_exists.first():
                return jsonify({"error": "Lifting material already exists"}), 409

            # Insere novo registro
            result = current_session.execute(
                text("INSERT INTO tbl_lifting_shackles (id_lifting_material) VALUES (:id) RETURNING id_lifting_material"),
                {"id": data.get("id_lifting_material")}
            )
        elif lifting_type == 'Spreader':
            # Verifica se o id_lifting_material já existe na tabela tbl_cargo_condition_wood
            already_exists = current_session.execute(
                text("SELECT 1 FROM tbl_lifting_spreader WHERE id_lifting_material = :id"),
                {"id": data.get("id_lifting_material")}
            )

            if already_exists.first():
                return jsonify({"error": "Lifting material already exists"}), 409

            # Insere novo registro
            result = current_session.execute(
                text("INSERT INTO tbl_lifting_spreader (id_lifting_material) VALUES (:id) RETURNING id_lifting_material"),
                {"id": data.get("id_lifting_material")}
            )
        elif lifting_type == 'Chain':
            # Verifica se o id_lifting_material já existe na tabela tbl_cargo_condition_wood
            already_exists = current_session.execute(
                text("SELECT 1 FROM tbl_lifting_chain WHERE id_lifting_material = :id"),
                {"id": data.get("id_lifting_material")}
            )

            if already_exists.first():
                return jsonify({"error": "Lifting material already exists"}), 409

            # Insere novo registro
            result = current_session.execute(
                text("INSERT INTO tbl_lifting_chain (id_lifting_material) VALUES (:id) RETURNING id_lifting_material"),
                {"id": data.get("id_lifting_material")}
            )
        elif lifting_type == 'Hook':
            # Verifica se o id_lifting_material já existe na tabela tbl_cargo_condition_wood
            already_exists = current_session.execute(
                text("SELECT 1 FROM tbl_lifting_hook WHERE id_lifting_material = :id"),
                {"id": data.get("id_lifting_material")}
            )

            if already_exists.first():
                return jsonify({"error": "Lifting material already exists"}), 409

            # Insere novo registro
            result = current_session.execute(
                text("INSERT INTO tbl_lifting_hook (id_lifting_material) VALUES (:id) RETURNING id_lifting_material"),
                {"id": data.get("id_lifting_material")}
            )
        elif lifting_type == 'Master Link':
            # Verifica se o id_lifting_material já existe na tabela tbl_cargo_condition_wood
            already_exists = current_session.execute(
                text("SELECT 1 FROM tbl_lifting_link WHERE id_lifting_material = :id"),
                {"id": data.get("id_lifting_material")}
            )

            if already_exists.first():
                return jsonify({"error": "Lifting material already exists"}), 409

            # Insere novo registro
            result = current_session.execute(
                text("INSERT INTO tbl_lifting_link (id_lifting_material) VALUES (:id) RETURNING id_lifting_material"),
                {"id": data.get("id_lifting_material")}
            )
        else:
            return jsonify({"error": "Lifting type not found"}), 404
        
        current_session.commit()
        id_lifting_material = result.fetchone()._mapping["id_lifting_material"]

        return jsonify({
            "message": "Lifting material created successfully", 
            "id": id_lifting_material
        }), 201

    except Exception as e:
        current_session.rollback()
        logger.error(f"Error creating lifting inspection: {str(e)}")
        return jsonify({"error": str(e)}), 500

    finally:
        current_session.close()