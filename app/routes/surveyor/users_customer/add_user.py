from flask import jsonify, request
from sqlalchemy import text
from werkzeug.security import generate_password_hash
from marshmallow import ValidationError

from app.services import Session
from . import users_customer_bp
from .schema import user_customer_schema

@users_customer_bp.route('/', methods=['POST'])
def add_user():
    try:
        data = user_customer_schema.load(request.json)

        current_session = Session()

        try:
            current_users = current_session.execute(
                text("SELECT * FROM tbl_user_customer WHERE email = :email"),
                {
                    "email": data.get("email")
                }
            )

            if list(current_users):
                return jsonify({"error": "Such user already signed up in the system."}), 400
            
            matching_users_result = current_session.execute(
                text("SELECT id_customer FROM tbl_customer_employee WHERE email = :email"),
                {
                    "email": data.get("email")
                }
            )

            matching_users = [dict(row) for row in matching_users_result.mappings()];
            
            if not matching_users:
                return jsonify({"error": "Email not authorized - unknown employee."}), 400
            
            id_customer = matching_users[0]["id_customer"]

            hashed_password = generate_password_hash(data.get("password"))

            result = current_session.execute(
                text("INSERT INTO tbl_user_customer (email, password, id_customer) VALUES (:email, :password, :id_customer) RETURNING id_user"),
                {
                    "email": data.get("email"), 
                    "password": hashed_password,
                    "id_customer": id_customer
                }
            )

            current_session.commit()

            last_id = result.fetchone()._mapping["id_user"]

            return jsonify({"message": "User created successfully", "id": last_id}), 201
        except Exception as e:
            current_session.rollback()
            return jsonify({"error": str(e)}), 500
        finally:
            current_session.close()
    except ValidationError as e:
        return jsonify({"error": "Validation Error", "details": e.messages}), 400
