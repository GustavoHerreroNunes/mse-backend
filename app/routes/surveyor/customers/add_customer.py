from flask import request, jsonify
from sqlalchemy import text
from app.services import Session
from . import customers_bp, logger
from .schema import customer_schema

@customers_bp.route('/', methods=['POST'])
def add_customer():
    """Add new customer"""
    data = customer_schema.load(request.json)
    current_session = Session()
    
    try:
        existing = current_session.execute(
            text("SELECT customer_id FROM tbl_customer WHERE customer_name = :name"),
            {"name": data.get("customer_name")}
        )

        if list(existing):
            return jsonify({"error": "A customer with this name already exists"}), 409

        result = current_session.execute(
            text("INSERT INTO tbl_customer (customer_name) VALUES (:name) RETURNING customer_id"),
            {"name": data.get("customer_name")}
        )

        current_session.commit()
        customer_id = result.fetchone()._mapping["customer_id"]

        return jsonify({
            "message": "Customer created successfully", 
            "id": customer_id,
            "name": data.get("customer_name")
        }), 201
    except Exception as e:
        current_session.rollback()
        logger.error(f"Error creating customer: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()