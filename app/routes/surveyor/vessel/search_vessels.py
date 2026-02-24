from flask import jsonify, request
from sqlalchemy import text

from app.services import Session
from . import vessel_bp, logger

@vessel_bp.route('/search', methods=['GET'])
def search_vessels():
    """Search vessels by name"""
    logger.info("GET /vessels/search request received")
    
    search_term = request.args.get('vesselName')
    if not search_term:
        return jsonify({"error": "Search term 'vesselName' is required"}), 400
    
    session = Session()
    
    try:
        # Search vessels with name containing the search term (case insensitive)
        search_query = text("""
            SELECT * FROM tbl_vessel 
            WHERE LOWER(vessel_name) LIKE LOWER(:search_pattern)
        """)
        
        search_result = session.execute(
            search_query, 
            {"search_pattern": f"%{search_term}%"}
        )
        
        result = [dict(row) for row in search_result.mappings()]
        
        logger.info(f"Found {len(result)} vessels matching '{search_term}'")
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Error in search_vessels: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
    finally:
        session.close()
