from flask import jsonify
from sqlalchemy import text

from app.services import Session
from . import statement_of_facts_bp, logger
from .schema import statement_of_facts_list_schema

@statement_of_facts_bp.route('/demanda/<int:demanda_id>', methods=['GET'])
def get_statement_of_facts_by_demanda(demanda_id):
    """Get all statement of facts entries for a specific demanda"""
    current_session = Session()
    
    try:
        result = current_session.execute(
            text("""
                SELECT             
                    event_id, 
                    demanda_id, 
                    location, 
                    preliminary_status, 
                    preliminary_timestamp_start,
                    location_status, 
                    location_timestamp_start, 
                    task_status, 
                    task_timestamp_start,
                    ship_status, 
                    ship_timestamp_start, 
                    attendance_status, 
                    attendance_timestamp_start,
                    cargo_status, 
                    cargo_timestamp_start, 
                    preliminary_timestamp_end, 
                    location_timestamp_end,
                    task_timestamp_end, 
                    ship_timestamp_end, 
                    attendance_timestamp_end, 
                    cargo_timestamp_end
                FROM tbl_statement
                WHERE demanda_id = :demanda_id 
            """),
            {"demanda_id": demanda_id}
        )
        
        return statement_of_facts_list_schema.dumps(result)
    except Exception as e:
        current_session.rollback()
        logger.error(f"Error retrieving statement of facts by survey: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()
