from flask import jsonify
from sqlalchemy import text

from app.services import Session
from . import statement_of_facts_bp, logger
from .schema import statement_of_facts_cargo_list_schema

@statement_of_facts_bp.route('/demanda/cargo/<int:cargo_id>', methods=['GET'])
def get_statement_of_facts_by_cargo(cargo_id):
    """Get all statement of facts entries for a specific cargo"""
    current_session = Session()
    
    try:
        result = current_session.execute(
            text("""
                SELECT             
                    event_id, 
                    cargo_id, 
                    location, 
                    inspection_status, 
                    inspection_timestamp_start,
                    items_status, 
                    items_timestamp_start, 
                    operation_status, 
                    operation_timestamp_start,
                    storage_status, 
                    storage_timestamp_start, 
                    material_status, 
                    material_timestamp_start,
                    board_status, 
                    board_timestamp_start, 
                    inspection_timestamp_end, 
                    items_timestamp_end,
                    operation_timestamp_end, 
                    storage_timestamp_end, 
                    material_timestamp_end, 
                    board_timestamp_end
                FROM tbl_statement_cargo
                WHERE cargo_id = :cargo_id
            """),
            {"cargo_id": cargo_id}
        )
        
        return statement_of_facts_cargo_list_schema.dumps(result)
    except Exception as e:
        current_session.rollback()
        logger.error(f"Error retrieving statement of facts by survey: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()
