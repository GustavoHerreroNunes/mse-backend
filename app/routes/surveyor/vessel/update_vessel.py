from flask import request, jsonify
from sqlalchemy import text

from app.services import Session
from . import vessel_bp, logger, VALID_CRANE_POSITIONS, FIELDS_FOR_VESSELS

@vessel_bp.route('/<int:vessel_id>', methods=['PUT'])
def update_vessel(vessel_id):
    """Update a vessel with all its cranes and SWL capacities"""
    logger.info(f"PUT /vessels/{vessel_id} request received")
    
    session = Session()
    
    try:
        # Verify vessel exists
        vessel_query = text("SELECT * FROM tbl_vessel WHERE vessel_id = :vessel_id")
        vessel_result = session.execute(vessel_query, {"vessel_id": vessel_id})
        vessel_rows = [dict(row) for row in vessel_result.mappings()]
        
        if not vessel_rows:
            return jsonify({"error": "Vessel not found"}), 404
        
        current_vessel = vessel_rows[0]
        data = request.json
        
        # Verify vessel type hasn't changed from original value
        if 'vessel_type' in data and data['vessel_type'] != current_vessel['vessel_type']:
            return jsonify({"error": "Vessel type cannot be changed from what was previously created"}), 400
        
        # Use vessel type to determine which fields to validate
        vessel_type = current_vessel['vessel_type'].lower()
        all_fields = FIELDS_FOR_VESSELS["all"]
        type_fields = FIELDS_FOR_VESSELS.get(vessel_type.lower(), {"numeric": [], "non-numeric": []})
        
        # Verify numeric fields are greater than zero
        # numeric_fields = all_fields["numeric"] + type_fields["numeric"]
        
        # for field in numeric_fields:
        #     if field in data and data[field] is not None and data[field] <= 0:
        #         return jsonify({"error": f"Error: Vessel measure smaller or equal to zero - {field}"}), 400
        
        # # Verify loaded_draft and light_draft relationship if both are provided or if one is being updated
        # loaded_draft = data.get('loaded_draft', current_vessel['loaded_draft'])
        # light_draft = data.get('light_draft', current_vessel['light_draft'])
        
        # if loaded_draft < light_draft:
        #     return jsonify({"error": "Error: Loaded_draft must to be greater than or equal to Light Draft"}), 400
        
        # Build update query dynamically based on provided fields for vessel
        update_fields = []
        params = {"vessel_id": vessel_id}
        new_crane_ids = []
        new_swl_ids = []
        
        # Get all possible fields for this vessel type
        all_possible_fields = all_fields["non-numeric"] + all_fields["numeric"] + type_fields["non-numeric"] + type_fields["numeric"]
        
        # Remove vessel_id to prevent it from being updated
        all_possible_fields = [f for f in all_possible_fields if f != "vessel_id"]
        
        for field in all_possible_fields:
            if field in data:
                update_fields.append(f"{field} = :{field}")
                params[field] = data[field]
        
        if update_fields:
            vessel_update_query = f"""
                UPDATE tbl_vessel SET {', '.join(update_fields)} 
                WHERE vessel_id = :vessel_id
            """
            session.execute(text(vessel_update_query), params)
            logger.info(f"Vessel ID {vessel_id} updated successfully")
        
        # Process cranes if they're in the request
        if "cranes" in data and isinstance(data["cranes"], list):
            
            # Get existing cranes for this vessel
            existing_cranes_query = text("SELECT crane_id FROM tbl_vessel_crane WHERE vessel_id = :vessel_id")
            existing_cranes_result = session.execute(existing_cranes_query, {"vessel_id": vessel_id})
            existing_crane_ids = [row['crane_id'] for row in existing_cranes_result.mappings()]
            
            # Track crane IDs we've processed to identify which ones to keep
            processed_crane_ids = []
            
            for crane_data in data["cranes"]:
                # If crane has ID, update it if it belongs to this vessel
                if "crane_id" in crane_data and crane_data["crane_id"] in existing_crane_ids:
                    crane_id = crane_data["crane_id"]
                    processed_crane_ids.append(crane_id)
                    
                    # Validate position
                    if "position_on_vessel" not in crane_data:
                        return jsonify({"error": "Position on vessel is required for all cranes"}), 400
                    
                    if crane_data["position_on_vessel"] not in VALID_CRANE_POSITIONS:
                        return jsonify({"error": f"Invalid crane position: {crane_data['position_on_vessel']}"}), 400
                    
                    # Update crane
                    crane_update_query = """
                        UPDATE tbl_vessel_crane 
                        SET position_on_vessel = :position_on_vessel 
                        WHERE crane_id = :crane_id
                    """
                    session.execute(
                        text(crane_update_query), 
                        {
                            "crane_id": crane_id,
                            "position_on_vessel": crane_data["position_on_vessel"]
                        }
                    )
                    logger.info(f"Crane ID {crane_id} updated successfully")
                
                # If crane has no ID, create new one
                elif "crane_id" not in crane_data:
                    # Validate position
                    if "position_on_vessel" not in crane_data:
                        return jsonify({"error": "Position on vessel is required for all cranes"}), 400
                    
                    if crane_data["position_on_vessel"] not in VALID_CRANE_POSITIONS:
                        return jsonify({"error": f"Invalid crane position: {crane_data['position_on_vessel']}"}), 400
                    
                    # Create new crane
                    crane_query = """
                        INSERT INTO tbl_vessel_crane (
                            vessel_id, position_on_vessel
                        ) VALUES (
                            :vessel_id, :position_on_vessel
                        ) RETURNING crane_id
                    """
                    crane_result = session.execute(
                        text(crane_query), 
                        {
                            "vessel_id": vessel_id,
                            "position_on_vessel": crane_data["position_on_vessel"]
                        }
                    )
                    
                    crane_id = [dict(row) for row in crane_result.mappings()][0]["crane_id"]
                    processed_crane_ids.append(crane_id)
                    new_crane_ids.append(crane_id)
                    logger.info(f"New crane created with ID: {crane_id}")
                
                print(crane_data)

                # Process SWL capacities if they exist
                if crane_id and "swl_capacities" in crane_data and isinstance(crane_data["swl_capacities"], list):
                    # Get existing SWL capacities for this crane
                    existing_swl_query = text("SELECT swl_capacity_id FROM tbl_swl_capacities WHERE crane_id = :crane_id")
                    existing_swl_result = session.execute(existing_swl_query, {"crane_id": crane_id})
                    existing_swl_ids = [row['swl_capacity_id'] for row in existing_swl_result.mappings()]
                    
                    # Track SWL IDs we've processed to identify which ones to keep
                    processed_swl_ids = []
                    
                    for swl_data in crane_data["swl_capacities"]:
                        print('Found SWL_DATA')
                        print(swl_data)
                        # If SWL has ID, update it if it belongs to this crane
                        if "swl_capacity_id" in swl_data and swl_data["swl_capacity_id"] in existing_swl_ids:
                            swl_capacity_id = swl_data["swl_capacity_id"]
                            print(f"Id Found: {swl_capacity_id}")
                            processed_swl_ids.append(swl_capacity_id)
                            
                            # Validate SWL data
                            required_fields = ["weight", "radius_start", "radius_end"]
                            for field in required_fields:
                                if field not in swl_data:
                                    return jsonify({"error": f"{field} is required for all SWL capacities"}), 400
                                
                                # Verify numeric fields are greater than zero
                                if swl_data[field] <= 0 and field != "radius_start":
                                    return jsonify({"error": f"Error: SWL capacity measure smaller or equal to zero - {field}"}), 400
                            
                            # Update SWL capacity
                            swl_update_query = """
                                UPDATE tbl_swl_capacities 
                                SET weight = :weight, radius_start = :radius_start, radius_end = :radius_end 
                                WHERE swl_capacity_id = :swl_capacity_id
                            """
                            session.execute(
                                text(swl_update_query), 
                                {
                                    "swl_capacity_id": swl_capacity_id,
                                    "weight": swl_data["weight"],
                                    "radius_start": swl_data["radius_start"],
                                    "radius_end": swl_data["radius_end"]
                                }
                            )
                            logger.info(f"SWL capacity ID {swl_capacity_id} updated successfully")
                        
                        # If SWL has no ID, create new one
                        elif "swl_capacity_id" not in swl_data:
                            print("No id found")
                            # Validate SWL data
                            if not all(key in swl_data for key in ["weight", "radius_start", "radius_end"]):
                                return jsonify({"error": "Weight, radius_start, and radius_end are required for all SWL capacities"}), 400
                            
                            # Verify numeric fields are greater than zero
                            for field in ["weight", "radius_start", "radius_end"]:
                                if swl_data[field] <= 0 and field != "radius_start":
                                    return jsonify({"error": f"Error: SWL capacity measure smaller or equal to zero - {field}"}), 400
                            
                            # Create SWL capacity
                            swl_query = """
                                INSERT INTO tbl_swl_capacities (
                                    crane_id, weight, radius_start, radius_end
                                ) VALUES (
                                    :crane_id, :weight, :radius_start, :radius_end
                                ) RETURNING swl_capacity_id
                            """
                            print(swl_query)

                            swl_result = session.execute(
                                text(swl_query), 
                                {
                                    "crane_id": crane_id,
                                    "weight": swl_data["weight"],
                                    "radius_start": swl_data["radius_start"],
                                    "radius_end": swl_data["radius_end"]
                                }
                            )
                            
                            swl_capacity_id = [dict(row) for row in swl_result.mappings()][0]["swl_capacity_id"]
                            processed_swl_ids.append(swl_capacity_id)
                            new_swl_ids.append(swl_capacity_id)
                            logger.info(f"New SWL capacity created with ID: {swl_capacity_id}")
                        
                        elif "swl_capacity_id" in swl_data and swl_data["swl_capacity_id"] not in existing_swl_ids:
                            return jsonify({"error": "Swl capacity not found for the specified crane."}), 400
        session.commit()
        return jsonify({
            "message": "Vessel and all related data updated successfully",
            "crane_ids": new_crane_ids,
            "swl_capacity_ids": new_swl_ids    
        }), 200
        
    except Exception as e:
        logger.error(f"Error in update_vessel: {str(e)}")
        session.rollback()
        return jsonify({"error": str(e)}), 500
    
    finally:
        session.close()
