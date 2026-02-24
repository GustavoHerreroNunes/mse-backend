from flask import jsonify
from sqlalchemy import text

from app.services import Session
from . import vessel_bp, logger

@vessel_bp.route('/', methods=['GET'])
def get_all_vessels():
    """Retrieve all vessels from the database"""
    logger.info("GET /vessels request received")

    current_session = Session()

    try:
        vessels = current_session.execute(
            text("SELECT * FROM tbl_vessel ORDER BY vessel_name"),
        )
        logger.info("Database query executed")
        result = [dict(row) for row in vessels.mappings()]
        logger.info(f"Returning {len(result)} vessels")
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error in get_all_vessels: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()