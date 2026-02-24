from flask import request, jsonify
from sqlalchemy import text

from app.services import Session
from . import vessel_bp, logger

@vessel_bp.route('/<int:vessel_id>/cranes/<int:crane_id>/swl/<int:swl_capacity_id>', methods=['PUT'])
def update_swl_capacity(vessel_id, crane_id, swl_capacity_id):
    """Update a specific SWL capacity for a specific crane on a specific vessel"""
    logger.info(f"PUT /vessels/{vessel_id}/cranes/{crane_id}/swl/{swl_capacity_id} request received")
    
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
            text("SELECT * FROM tbl_swl_capacities WHERE swl_capacity_id = :swl_capacity_id AND crane_id = :crane_id"),
            {"swl_capacity_id": swl_capacity_id, "crane_id": crane_id}
        )
        swl_result = [dict(row) for row in swl.mappings()]
        
        if not swl_result:
            return jsonify({"error": "SWL capacity not found or does not belong to the specified crane"}), 404
        
        data = request.json
        
        # Validate SWL data
        required_fields = ["weight", "radius_start", "radius_end"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"{field} is required for updating an SWL capacity"}), 400
            
            # Verify numeric fields are greater than zero
            if data[field] <= 0 and field != "radius_start":
                return jsonify({"error": f"Error: SWL capacity measure smaller or equal to zero - {field}"}), 400
        
        update_query = """
            UPDATE tbl_swl_capacities 
            SET weight = :weight, radius_start = :radius_start, radius_end = :radius_end 
            WHERE swl_capacity_id = :swl_capacity_id
        """
        
        current_session.execute(
            text(update_query), 
            {
                "swl_capacity_id": swl_capacity_id,
                "weight": data["weight"],
                "radius_start": data["radius_start"],
                "radius_end": data["radius_end"]
            }
        )

        current_session.commit()
        
        logger.info(f"SWL capacity ID {swl_capacity_id} updated successfully")
        return jsonify({"message": "SWL capacity updated successfully"}), 200
        
    except Exception as e:
        logger.error(f"Error in update_swl_capacity: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
    finally:
        current_session.close()
