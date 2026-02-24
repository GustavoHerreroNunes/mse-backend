from sqlalchemy import text

from .. import logger

def create_crane(vessel_id, crane_data, session):
    """Create a crane record in the database"""
    
    try:
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
        logger.info(f"Crane created with ID: {crane_id}")
        return crane_id
    except Exception as e:
        logger.error(f"Error creating crane: {str(e)}")
        raise