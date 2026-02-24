from flask import jsonify
from sqlalchemy import text

from app.services import Session
from . import vessel_bp, logger

@vessel_bp.route('/<int:vessel_id>', methods=['GET'])
def get_vessel_by_id(vessel_id):
    """Retrieve a specific vessel by ID with all its cranes and SWL capacities"""
    logger.info(f"GET /vessels/{vessel_id} request received")
    
    session = Session()
    
    try:
        # Get vessel data
        vessel_query = text("SELECT * FROM tbl_vessel WHERE vessel_id = :vessel_id ORDER BY vessel_id")
        vessel_result = session.execute(vessel_query, {"vessel_id": vessel_id})
        vessel_rows = [dict(row) for row in vessel_result.mappings()]

        if not vessel_rows:
            return jsonify({"error": "Vessel not found"}), 404
        
        vessel_data = vessel_rows[0]
        
        # Get crane data for this vessel
        cranes_query = text("SELECT * FROM tbl_vessel_crane WHERE vessel_id = :vessel_id ORDER BY crane_id")
        cranes_result = session.execute(cranes_query, {"vessel_id": vessel_id})
        cranes_data = [dict(row) for row in cranes_result.mappings()]
        
        # For each crane, get its SWL capacities
        for crane in cranes_data:
            swl_query = text("SELECT * FROM tbl_swl_capacities WHERE crane_id = :crane_id ORDER BY swl_capacity_id")
            swl_result = session.execute(swl_query, {"crane_id": crane["crane_id"]})
            crane["swl_capacities"] = [dict(row) for row in swl_result.mappings()]
        
        # Add cranes to vessel data
        vessel_data["cranes"] = cranes_data
        
        logger.info(f"Retrieved vessel ID {vessel_id} with {len(cranes_data)} cranes")
        return jsonify(vessel_data)
    
    except Exception as e:
        logger.error(f"Error in get_vessel_by_id: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
    finally:
        session.close()