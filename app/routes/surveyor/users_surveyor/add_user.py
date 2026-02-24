from flask import jsonify, request
from sqlalchemy import text
from werkzeug.security import generate_password_hash
from marshmallow import ValidationError

from app.services import Session
from . import users_surveyor_bp
from .schema import user_surveyor_schema

@users_surveyor_bp.route('/', methods=['POST'])
def add_user():
    try:
        data = user_surveyor_schema.load(request.json)

        current_session = Session()

        try:
            current_users = current_session.execute(
                text("SELECT * FROM tbl_user_surveyor WHERE email = :email"),
                {
                    "email": data.get("email")
                }
            )

            if list(current_users):
                return jsonify({"error": "Such user already signed up in the system."}), 400
            
            matching_users_result = current_session.execute(
                text("SELECT employee_name FROM tbl_employees WHERE employee_email = :email"),
                {
                    "email": data.get("email")
                }
            )

            matching_users = [dict(row) for row in matching_users_result.mappings()];

            if not matching_users:
                return jsonify({"error": "Email not authorized - unknown employee."}), 400
            
            display_name = matching_users[0]["employee_name"]

            hashed_password = generate_password_hash(data.get("password"));

            result = current_session.execute(
                text("INSERT INTO tbl_user_surveyor (display_name, email, password) VALUES (:display_name, :email, :password) RETURNING id"),
                {
                    "display_name": display_name, 
                    "email": data.get("email"), 
                    "password": hashed_password
                }
            )

            current_session.commit()

            last_id = result.fetchone()._mapping["id"]

            return jsonify({"message": "User created successfully", "id": last_id}), 201
        except Exception as e:
            current_session.rollback()
            return jsonify({"error": str(e)}), 500
        finally:
            current_session.close()
    except ValidationError as e:
        return jsonify({"error": "Validation Error", "details": e.messages}), 400
