from flask import jsonify
from sqlalchemy import text

from app.services import Session
from . import vessel_bp, logger

@vessel_bp.route('/<int:vessel_id>', methods=['DELETE'])
def delete_vessel(vessel_id):
    """Delete a specific vessel and all its related data (cranes and SWL capacities)"""
    logger.info(f"DELETE /vessels/{vessel_id} request received")
    
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
        
        # Delete vessel (cascade will handle cranes and SWL capacities)
        current_session.execute(
            text("DELETE FROM tbl_vessel WHERE vessel_id = :vessel_id"),
            {"vessel_id": vessel_id}
        )
        
        current_session.commit()

        logger.info(f"Vessel ID {vessel_id} and all related data deleted successfully")
        return jsonify({"message": "Vessel and all related data deleted successfully"}), 200
        
    except Exception as e:
        logger.error(f"Error in delete_vessel: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
    finally:
        current_session.close()
