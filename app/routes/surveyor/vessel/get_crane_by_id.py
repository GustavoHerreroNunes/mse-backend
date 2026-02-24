from flask import jsonify
from sqlalchemy import text

from app.services import Session
from . import vessel_bp, logger

@vessel_bp.route('/<int:vessel_id>/cranes/<int:crane_id>', methods=['GET'])
def get_crane_by_id(vessel_id, crane_id):
    """Retrieve a specific crane for a specific vessel"""

    logger.info(f"GET /vessels/{vessel_id}/cranes/{crane_id} request received")
    
    current_session = Session();

    try:
        # First verify that the vessel exists
        vessel = current_session.execute(
            text("SELECT vessel_id FROM tbl_vessel WHERE vessel_id = :vessel_id"),
            {"vessel_id": vessel_id}
        )
        vessel_result = [dict(row) for row in vessel.mappings()]
        
        if not vessel_result:
            return jsonify({"error": "Vessel not found"}), 404
        
        # Get the specific crane and verify it belongs to the vessel
        crane = current_session.execute(
            text("SELECT * FROM tbl_vessel_crane WHERE crane_id = :crane_id AND vessel_id = :vessel_id"),
            {"crane_id": crane_id, "vessel_id": vessel_id}
        )
        result = [dict(row) for row in crane.mappings()]
        
        if not result:
            return jsonify({"error": "Crane not found or does not belong to the specified vessel"}), 404
        
        logger.info(f"Returning data for crane ID {crane_id} on vessel ID {vessel_id}")
        return jsonify(result[0])
    
    except Exception as e:
        logger.error(f"Error in get_crane_by_id: {str(e)}")
        return jsonify({"error": str(e)}), 500
