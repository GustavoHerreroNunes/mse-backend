from flask import jsonify
from sqlalchemy import text

from app.services import Session
from . import logger, settings_bp
from .schema import settings_schema

@settings_bp.route('/app_version', methods=['GET'])
def get_app_version():
    logger.info("GET /app_version request received")

    current_session = Session()

    try:
        settings = current_session.execute(
            text("SELECT * FROM tbl_settings where id_settings = 'APP_V'"),
        ).fetchone()
        logger.info("Database query executed")
        if settings:
            result = settings_schema.dump(settings)
            logger.info("Returning 1 setting")
            return jsonify(result)
        else:
            logger.info("No settings found")
            return jsonify({}), 404
    except Exception as e:
        logger.error(f"Error in get_settings: {str(e)}")
        current_session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()