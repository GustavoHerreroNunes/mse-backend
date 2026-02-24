from flask import jsonify
from sqlalchemy import text

from app.services import Session
from . import logger, users_customer_bp
from .schema import user_customer_list_schema

@users_customer_bp.route('/', methods=['GET'])
def get_users():
    logger.info("GET /users_customer request received")

    current_session = Session()

    try:
        users = current_session.execute(
            text("SELECT * FROM tbl_user_customer"),
        )
        logger.info("Database query executed")
        result = user_customer_list_schema.dump(users)
        logger.info(f"Returning {len(result)} users")
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in get_users: {str(e)}")
        current_session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()