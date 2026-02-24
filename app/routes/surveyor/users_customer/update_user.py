from flask import jsonify, request
from sqlalchemy import text
from werkzeug.security import generate_password_hash
from marshmallow import ValidationError

from app.services import Session
from . import logger, users_customer_bp
from .schema import user_customer_schema

@users_customer_bp.route('/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        data = user_customer_schema.load(request.json, partial=True)
        current_session = Session()
        
        try:
            # First check if user exists
            user_exists = current_session.execute(
                text("SELECT id_user FROM tbl_user_customer WHERE id_user = :id"),
                {"id": id}
            )
            
            if not list(user_exists):
                return jsonify({"error": "User not found"}), 404
                
            update_fields = []
            params = {"id": id}
            
            if data.get("password"):
                update_fields.append("password = :password")
                params["password"] = generate_password_hash(data.get("password"))
                
            if update_fields:
                query = f"UPDATE tbl_user_customer SET {', '.join(update_fields)} WHERE id_user = :id"
                current_session.execute(text(query), params)
                current_session.commit()
                
            return jsonify({"message": "User updated successfully"}), 200
        except Exception as e:
            current_session.rollback()
            logger.error(f"Error updating user: {str(e)}")
            return jsonify({"error": str(e)}), 500
        finally:
            current_session.close()
    except ValidationError as e:
        return jsonify({"error": "Validation Error", "details": e.messages}), 400