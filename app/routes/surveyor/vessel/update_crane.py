from flask import request, jsonify
from sqlalchemy import text

from app.services import Session
from . import vessel_bp, logger, VALID_CRANE_POSITIONS

@vessel_bp.route('/<int:vessel_id>/cranes/<int:crane_id>', methods=['PUT'])
def update_crane(vessel_id, crane_id):
    """Update a specific crane on a specific vessel"""
    logger.info(f"PUT /vessels/{vessel_id}/cranes/{crane_id} request received")

    current_session = Session()
    try:
        # Verify vessel exists
        vessel = current_session.execute(
            text("SELECT vessel_id FROM tbl_vessel WHERE vessel_id = :vessel_id"),
            {"vessel_id": vessel_id}
        )
        vessel_result = [dict(row) for row in vessel.mappings()]
        
        if not vessel_result:
            return jsonify({"error": "Vessel not found"}), 404
        
        # Verify crane exists and belongs to the vessel
        crane = current_session.execute(
            text("SELECT * FROM tbl_vessel_crane WHERE crane_id = :crane_id AND vessel_id = :vessel_id"),
            {"crane_id": crane_id, "vessel_id": vessel_id}
        )
        crane_result = [dict(row) for row in crane.mappings()]
        
        if not crane_result:
            return jsonify({"error": "Crane not found or does not belong to the specified vessel"}), 404
        
        data = request.json
        
        # For cranes, we only update position_on_vessel
        if 'position_on_vessel' not in data:
            return jsonify({"error": "Position on vessel is required for updating a crane"}), 400
        
        if data['position_on_vessel'] not in VALID_CRANE_POSITIONS:
            return jsonify({"error": f"Invalid crane position: {data['position_on_vessel']}"}), 400
        
        update_query = """
            UPDATE tbl_vessel_crane 
            SET position_on_vessel = :position_on_vessel 
            WHERE crane_id = :crane_id
        """
        
        current_session.execute(
            text(update_query), 
            {
                "crane_id": crane_id,
                "position_on_vessel": data['position_on_vessel']
            }
        )

        current_session.commit()
        
        logger.info(f"Crane ID {crane_id} updated successfully")
        return jsonify({"message": "Crane updated successfully"}), 200
        
    except Exception as e:
        logger.error(f"Error in update_crane: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()
