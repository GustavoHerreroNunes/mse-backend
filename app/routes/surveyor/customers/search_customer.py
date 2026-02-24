from flask import request, jsonify
from sqlalchemy import text
from app.services import Session
from . import customers_bp, logger
from .schema import customer_list_schema

@customers_bp.route('/search', methods=['GET'])
def search_customer():
    """Search for customers matching the name provided"""
    search_parameter = request.args.get("name")
    if not search_parameter:
        return jsonify({"error": "Missing required query parameter 'name'"}), 400

    current_session = Session()
    try:
        customers = current_session.execute(
            text("SELECT * FROM tbl_customer WHERE LOWER(customer_name) LIKE LOWER(:search)"),
            {"search": f"%{search_parameter}%"}
        )
        return customer_list_schema.dumps(customers), 200
    except Exception as e:
        current_session.rollback()
        logger.error(f"Error retrieving customers for name '{search_parameter}': {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()
