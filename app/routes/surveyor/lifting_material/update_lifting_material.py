from flask import jsonify, request
from sqlalchemy import text
from marshmallow import ValidationError

from app.services import Session
from . import logger, lifting_material_bp
from .schema import lifting_material_schema

@lifting_material_bp.route('/<int:id_lifting_material>', methods=['PUT'])
def update_lifting_material(id_lifting_material):
    try:
        data = lifting_material_schema.load(request.json, partial=True)
        current_session = Session()

        try:
            # Verifica se o cargo existe
            cargo_exists = current_session.execute(
                text("SELECT id_lifting_material FROM tbl_lifting_material WHERE id_lifting_material = :id"),
                {"id": id_lifting_material}
            )

            if not list(cargo_exists):
                return jsonify({"error": "Lifting material not found"}), 404

            update_fields = []
            params = {"id": id_lifting_material}

            # Campos que podem ser atualizados
            fields_to_update = [
                "type", 
                "quantity",
                "weight", 
                "lenght"
            ]

            for field in fields_to_update:
                if field in data:
                    update_fields.append(f"{field} = :{field}")
                    params[field] = data[field]

            if update_fields:
                query = f"UPDATE tbl_lifting_material SET {', '.join(update_fields)} WHERE id_lifting_material = :id"
                current_session.execute(text(query), params)
                current_session.commit()

                return jsonify({"message": "Lifting material updated successfully"}), 200
            else:
                return jsonify({"message": "No fields provided for update"}), 400

        except Exception as e:
            current_session.rollback()
            logger.error(f"Error updating lifting material: {str(e)}")
            return jsonify({"error": str(e)}), 500
        finally:
            current_session.close()

    except ValidationError as e:
        return jsonify({"error": "Validation Error", "details": e.messages}), 400