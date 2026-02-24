from flask import jsonify
from sqlalchemy import text

from app.services import Session
from . import vessel_bp, logger

@vessel_bp.route('/<int:vessel_id>/cranes/<int:crane_id>', methods=['DELETE'])
def delete_crane(vessel_id, crane_id):
    """Delete a specific crane and all its SWL capacities"""
    logger.info(f"DELETE /vessels/{vessel_id}/cranes/{crane_id} request received")
    
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
            text("SELECT crane_id FROM tbl_vessel_crane WHERE crane_id = :crane_id AND vessel_id = :vessel_id"),
            {"crane_id": crane_id, "vessel_id": vessel_id}
        )
        crane_result = [dict(row) for row in crane.mappings()]
        
        if not crane_result:
            return jsonify({"error": "Crane not found or does not belong to the specified vessel"}), 404
        
        # Delete crane (cascade will handle SWL capacities)
        current_session.execute(
            text("DELETE FROM tbl_vessel_crane WHERE crane_id = :crane_id"),
            {"crane_id": crane_id}
        )

        current_session.commit()
        
        logger.info(f"Crane ID {crane_id} and all related SWL capacities deleted successfully")
        return jsonify({"message": "Crane and all related SWL capacities deleted successfully"}), 200
        
    except Exception as e:
        logger.error(f"Error in delete_crane: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
    finally:
        current_session.close()