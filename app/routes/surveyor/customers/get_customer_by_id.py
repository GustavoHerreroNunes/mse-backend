from flask import jsonify
from sqlalchemy import text
from app.services import Session
from . import customers_bp, logger
from .schema import customer_list_schema

@customers_bp.route('/<int:customer_id>', methods=['GET'])
def get_customer_by_id(customer_id):
    """Get customer by id"""
    current_session = Session()
    try:
        customer = current_session.execute(
            text("SELECT * FROM tbl_customer WHERE customer_id = :id"),
            {"id": customer_id}
        )
        result = customer_list_schema.dump(customer)

        if not result:
            return jsonify({"error": "Customer not found"}), 404
        return jsonify(result[0])
    except Exception as e:
        current_session.rollback()
        logger.error(f"Error retrieving customer with ID {customer_id}: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()
