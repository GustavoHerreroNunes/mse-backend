from sqlalchemy import text

from .. import logger

def create_swl_capacities(crane_id, swl_data, session):
    """Create a SWL capacity record in the database"""
    try:
        swl_query = """
            INSERT INTO tbl_swl_capacities (
                crane_id, weight, radius_start, radius_end
            ) VALUES (
                :crane_id, :weight, :radius_start, :radius_end
            )
            RETURNING swl_capacity_id
        """
        
        swl_results = session.execute(
            text(swl_query), 
            {
                "crane_id": crane_id,
                "weight": swl_data["weight"],
                "radius_start": swl_data["radius_start"],
                "radius_end": swl_data["radius_end"]
            }
        )
        
        logger.info(f"SWL capacity created for crane ID: {crane_id}")
        swl_id = [dict(row) for row in swl_results.mappings()][0]["swl_capacity_id"]
        return swl_id
    except Exception as e:
        logger.error(f"Error creating SWL capacity: {str(e)}")
        raise