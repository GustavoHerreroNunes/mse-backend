from flask import jsonify
from sqlalchemy import text
from app.services import Session
from . import customers_bp, logger
from .schema import customer_list_schema

@customers_bp.route('/', methods=['GET'])
def get_all_customers():
    """List all customers"""
    current_session = Session()
    try:
        customers = current_session.execute(
            text("SELECT * FROM tbl_customer ORDER BY customer_name")
        )
        return customer_list_schema.dumps(customers)
    except Exception as e:
        current_session.rollback()
        logger.error(f"Error retrieving customers: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()
