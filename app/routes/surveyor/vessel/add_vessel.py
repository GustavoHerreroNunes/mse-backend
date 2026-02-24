from flask import request, jsonify

from app.services import Session
from . import vessel_bp, logger, FIELDS_FOR_VESSELS
from .schema import VALID_VESSEL_TYPES, VALID_CRANE_POSITIONS, vessel_schema
from .utils.create_crane import create_crane
from .utils.create_swl_capacities import create_swl_capacities
from .utils.create_vessel import create_vessel

@vessel_bp.route('/', methods=['POST'])
def add_vessel():
    """Create a new Vessel with Cranes and SWL Capabilities if provided"""
    logger.info("POST /vessels request received")

    current_session = Session()

    try:
        data = request.json
        
        # Verify vessel type first since we need it for field validation
        if 'vessel_type' not in data:
            return jsonify({"error": "vessel_type is required"}), 400
            
        vessel_type = data['vessel_type'].lower()
        if vessel_type not in [vt.lower() for vt in VALID_VESSEL_TYPES]:
            return jsonify({"error": "Error: Unknown vessel type"}), 400
            
        # Get appropriate field lists based on vessel type
        # all_fields = FIELDS_FOR_VESSELS["all"]
        # type_fields = FIELDS_FOR_VESSELS.get(vessel_type.lower(), {"numeric": [], "non-numeric": []})
        
        # Check required vessel fields (all non-optional fields from the 'all' category)
        # required_non_numeric = all_fields["non-numeric"] + all_fields["numeric"] + type_fields["non-numeric"] + type_fields["numeric"]
        # for field in required_non_numeric:
        #     if field != "client_id" and field != "country_flag" and field != "year_of_built" and field != "imo_number" and field not in data:
        #         return jsonify({"error": f"Request Requirements not met: {field} is required"}), 400
        
        # Verify numeric fields are greater than zero
        # numeric_fields = all_fields["numeric"] + type_fields["numeric"]
        
        # for field in numeric_fields:
        #     if field in data and (data[field] is None or data[field] <= 0):
        #         return jsonify({"error": f"Error: Vessel measure smaller or equal to zero - {field}"}), 400
        
        # Verify loaded_draft is >= light_draft
        # if data['loaded_draft'] < data['light_draft']:
        #     return jsonify({"error": "Error: Loaded_draft must to be greater than or equal to Light Draft"}), 400

        # Create vessel
        vessel_id = create_vessel(data, current_session)

        new_crane_ids = []
        new_swl_ids = []
        
        # Create cranes if has_crane is True and cranes data is provided
        if data["has_crane"] and "cranes" in data and isinstance(data["cranes"], list):
            for crane_data in data["cranes"]:
                # Validate crane position
                if "position_on_vessel" not in crane_data:
                    return jsonify({"error": "Position on vessel is required for all cranes"}), 400
                
                if crane_data["position_on_vessel"] not in VALID_CRANE_POSITIONS:
                    return jsonify({"error": f"Invalid crane position: {crane_data['position_on_vessel']}"}), 400
                
                # Create crane
                crane_id = create_crane(vessel_id, crane_data, current_session)
                new_crane_ids.append(crane_id)

                # Create SWL capacities for the crane
                if "swl_capacities" in crane_data and isinstance(crane_data["swl_capacities"], list):
                    for swl_data in crane_data["swl_capacities"]:
                        # Validate SWL data
                        if not all(key in swl_data for key in ["weight", "radius_start", "radius_end"]):
                            return jsonify({"error": "Weight, radius_start, and radius_end are required for all SWL capacities"}), 400
                        
                        # Verify numeric fields are greater than zero
                        for field in ["weight", "radius_start", "radius_end"]:
                            if swl_data[field] <= 0 and field != "radius_start":
                                return jsonify({"error": f"Error: SWL capacity measure smaller or equal to zero - {field}"}), 400
                        
                        # Create SWL capacity
                        swl_id = create_swl_capacities(crane_id, swl_data, current_session)
                        new_swl_ids.append(swl_id)
        current_session.commit()

        return jsonify({
            "message": "Vessel created successfully", 
            "vessel_id": vessel_id,
            "crane_ids": new_crane_ids,
            "swl_capacity_ids": new_swl_ids
        }), 201
        
    except Exception as e:
        logger.error(f"Error in add_vessel: {str(e)}")
        current_session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()