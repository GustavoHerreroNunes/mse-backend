from flask import request, jsonify
from sqlalchemy import text
from app.services import Session
from . import relation_bp, logger
from .schema import relation_schema

@relation_bp.route('/', methods=['POST'])
def add_relation():
    """Add new relation"""
    data = relation_schema.load(request.json)
    current_session = Session()

    try:
        id_cargo = data.get("id_cargo")

        # Verifica se o cargo existe
        cargo_result = current_session.execute(
            text("SELECT cargo_id FROM tbl_cargo WHERE cargo_id = :id"),
            {"id": id_cargo}
        )
        if not list(cargo_result):
            return jsonify({"error": "Cargo not found"}), 404

        # Caso seja lista de lashings
        if data.get("id_lashing_material") != None:
            lashing_list = data.get("id_lashing_material")
            if not isinstance(lashing_list, list):
                return jsonify({"error": "id_lashing_material deve ser uma lista"}), 400

            # >>> Deleta vínculos antigos
            current_session.execute(
                text("DELETE FROM rlt_lashing_cargo WHERE id_cargo = :id_cargo"),
                {"id_cargo": id_cargo}
            )

            inserted_ids = []
            for id_lashing in lashing_list:
                # Valida se o lashing existe
                lashing_result = current_session.execute(
                    text("SELECT id_lashing_material FROM tbl_lashing_material WHERE id_lashing_material = :id"),
                    {"id": id_lashing}
                )
                if not list(lashing_result):
                    return jsonify({"error": f"Lashing {id_lashing} not found"}), 404

                query = """
                    INSERT INTO rlt_lashing_cargo (id_cargo, id_lashing_material)
                    VALUES (:id_cargo, :id_lashing_material)
                    RETURNING id_rlt
                """
                result = current_session.execute(
                    text(query), 
                    {"id_cargo": id_cargo, "id_lashing_material": id_lashing}
                )
                inserted_ids.append(result.fetchone()._mapping["id_rlt"])

            current_session.commit()

            return jsonify({
                "message": "Relations created successfully",
                "ids": inserted_ids
            }), 201

        # Caso seja lista de liftings
        elif data.get("id_lifting_material") != None:
            lifting_list = data.get("id_lifting_material")
            if not isinstance(lifting_list, list):
                return jsonify({"error": "id_lifting_material deve ser uma lista"}), 400

            # >>> Deleta vínculos antigos
            current_session.execute(
                text("DELETE FROM rlt_lifting_cargo WHERE id_cargo = :id_cargo"),
                {"id_cargo": id_cargo}
            )

            inserted_ids = []
            for id_lifting in lifting_list:
                # Valida se o lifting existe
                lifting_result = current_session.execute(
                    text("SELECT id_lifting_material FROM tbl_lifting_material WHERE id_lifting_material = :id"),
                    {"id": id_lifting}
                )
                if not list(lifting_result):
                    return jsonify({"error": f"Lifting {id_lifting} not found"}), 404

                query = """
                    INSERT INTO rlt_lifting_cargo (id_cargo, id_lifting_material)
                    VALUES (:id_cargo, :id_lifting_material)
                    RETURNING id_rlt
                """
                result = current_session.execute(
                    text(query), 
                    {"id_cargo": id_cargo, "id_lifting_material": id_lifting}
                )
                inserted_ids.append(result.fetchone()._mapping["id_rlt"])

            current_session.commit()

            return jsonify({
                "message": "Relations created successfully",
                "ids": inserted_ids
            }), 201

        else:
            return jsonify({"error": "Required fields: id_lashing_material OR id_lifting_material"}), 400

    except Exception as e:
        current_session.rollback()
        logger.error(f"Error creating relation: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()
