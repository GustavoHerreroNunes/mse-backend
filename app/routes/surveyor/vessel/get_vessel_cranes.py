from flask import jsonify
from sqlalchemy import text

from app.services import Session
from . import vessel_bp, logger

@vessel_bp.route('/<int:vessel_id>/cranes', methods=['GET'])
def get_vessel_cranes(vessel_id):
    """Retrieve all cranes for a specific vessel"""

    logger.info(f"GET /vessels/{vessel_id}/cranes request received")

    current_session = Session()
    
    try:
        # First verify that the vessel exists
        vessel = current_session.execute(
            text("SELECT vessel_id FROM tbl_vessel WHERE vessel_id = :vessel_id"),
            {"vessel_id": vessel_id}
        )
        vessel_result = [dict(row) for row in vessel.mappings()]
        
        if not vessel_result:
            return jsonify({"error": "Vessel not found"}), 404
        
        # Get all cranes for the vessel
        cranes = current_session.execute(
            text("SELECT * FROM tbl_vessel_crane WHERE vessel_id = :vessel_id"),
            {"vessel_id": vessel_id}
        )
        result = [dict(row) for row in cranes.mappings()]
        
        logger.info(f"Returning {len(result)} cranes for vessel ID {vessel_id}")
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Error in get_vessel_cranes: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()
