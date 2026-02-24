from flask import jsonify
from sqlalchemy import text

from app.services import Session
from . import vessel_bp, logger

@vessel_bp.route('/<int:vessel_id>/cranes/<int:crane_id>/swl/<int:swl_capacity_id>', methods=['DELETE'])
def delete_swl_capacity(vessel_id, crane_id, swl_capacity_id):
    """Delete a specific SWL capacity"""
    logger.info(f"DELETE /vessels/{vessel_id}/cranes/{crane_id}/swl/{swl_capacity_id} request received")
    
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
        
        # Verify SWL capacity exists and belongs to the crane
        swl = current_session.execute(
            text("SELECT swl_capacity_id FROM tbl_swl_capacities WHERE swl_capacity_id = :swl_capacity_id AND crane_id = :crane_id"),
            {"swl_capacity_id": swl_capacity_id, "crane_id": crane_id}
        )
        swl_result = [dict(row) for row in swl.mappings()]
        
        if not swl_result:
            return jsonify({"error": "SWL capacity not found or does not belong to the specified crane"}), 404
        
        # Delete SWL capacity
        current_session.execute(
            text("DELETE FROM tbl_swl_capacities WHERE swl_capacity_id = :swl_capacity_id"),
            {"swl_capacity_id": swl_capacity_id}
        )

        current_session.commit()
        
        logger.info(f"SWL capacity ID {swl_capacity_id} deleted successfully")
        return jsonify({"message": "SWL capacity deleted successfully"}), 200
        
    except Exception as e:
        logger.error(f"Error in delete_swl_capacity: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
    finally:
        current_session.close()
