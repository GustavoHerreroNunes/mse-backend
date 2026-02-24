from sqlalchemy import text

from .. import logger

def create_vessel(vessel_data, session):
    """Create a vessel record in the database"""
    try:
        vessel_query = """
            INSERT INTO tbl_vessel (
                imo_number, vessel_name, vessel_type, vessel_length, vessel_breadth, 
                vessel_beam, vessel_depth, loaded_draft, light_draft, gross_tonnage, 
                bollard_pull, has_crane, country_flag, year_of_built, dwt, client_id
            ) VALUES (
                :imo_number, :vessel_name, :vessel_type, :vessel_length, :vessel_breadth, 
                :vessel_beam, :vessel_depth, :loaded_draft, :light_draft, :gross_tonnage, 
                :bollard_pull, :has_crane, :country_flag, :year_of_built, :dwt, :client_id
            ) RETURNING vessel_id
        """
        
        params = {
            "imo_number": vessel_data.get("imo_number"),
            "vessel_name": vessel_data["vessel_name"],
            "vessel_type": vessel_data["vessel_type"],
            "vessel_length": vessel_data["vessel_length"],
            "vessel_breadth": vessel_data["vessel_breadth"],
            "vessel_beam": vessel_data["vessel_beam"],
            "vessel_depth": vessel_data["vessel_depth"],
            "loaded_draft": vessel_data["loaded_draft"],
            "light_draft": vessel_data["light_draft"],
            "gross_tonnage": vessel_data["gross_tonnage"],
            "bollard_pull": vessel_data.get("bollard_pull"),
            "has_crane": vessel_data["has_crane"],
            "country_flag": vessel_data.get("country_flag"),
            "year_of_built": vessel_data.get("year_of_built"),
            "dwt": vessel_data.get("dwt"),
            "client_id": vessel_data.get("client_id")
        }
        
        result = session.execute(text(vessel_query), params)
        vessel_id = [dict(row) for row in result.mappings()][0]["vessel_id"]
        logger.info(f"Vessel created with ID: {vessel_id}")
        return vessel_id
    except Exception as e:
        logger.error(f"Error creating vessel: {str(e)}")
        raise