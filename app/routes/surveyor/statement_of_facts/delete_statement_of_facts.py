from flask import jsonify
from sqlalchemy import text

from app.services import Session
from . import statement_of_facts_bp

@statement_of_facts_bp.route('/<int:event_id>', methods=['DELETE'])
def delete_statement_of_facts(event_id):
    """Delete statement of facts by event_id"""
    current_session = Session()
    
    try:
        # Check if statement of facts exists
        record = current_session.execute(
            text("SELECT event_id FROM tbl_statement WHERE event_id = :id"),
            {"id": event_id}
        )
        
        if not list(record):
            return jsonify({"error": "Statement of facts not found"}), 404
        
        current_session.execute(
            text("DELETE FROM tbl_statement WHERE event_id = :id"),
            {"id": event_id}
        )
        
        current_session.commit()
        
        return jsonify({"message": "Statement of facts deleted successfully"}), 200
    except Exception as e:
        current_session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()
