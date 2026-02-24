from flask import jsonify, request
from sqlalchemy import text
from werkzeug.security import generate_password_hash
from marshmallow import ValidationError

from app.services import Session
from . import logger, users_surveyor_bp
from .schema import user_surveyor_schema

@users_surveyor_bp.route('/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        data = user_surveyor_schema.load(request.json, partial=True)
        current_session = Session()
        
        try:
            # First check if user exists
            user_exists = current_session.execute(
                text("SELECT id FROM tbl_user_surveyor WHERE id = :id"),
                {"id": id}
            )
            
            if not list(user_exists):
                return jsonify({"error": "User not found"}), 404
            
            # Get just the email for employee verification
            email_result = current_session.execute(
                text("SELECT email FROM tbl_user_surveyor WHERE id = :id"),
                {"id": id}
            )
            email = email_result.fetchone()._mapping["email"]
            
            # Get employee name
            matching_users_result = current_session.execute(
                text("SELECT employee_name FROM tbl_employees WHERE employee_email = :email"),
                {"email": email}
            )
            matching_users = [dict(row) for row in matching_users_result.mappings()]
            
            # Determine display name
            display_name = data.get("display_name")
            if matching_users:
                display_name = matching_users[0]["employee_name"]
                
            update_fields = []
            params = {"id": id}
            
            if data.get("password"):
                update_fields.append("password = :password")
                params["password"] = generate_password_hash(data.get("password"))
                
            if display_name:
                update_fields.append("display_name = :display_name")
                params["display_name"] = display_name
                
            if update_fields:
                query = f"UPDATE tbl_user_surveyor SET {', '.join(update_fields)} WHERE id = :id"
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