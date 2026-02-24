from flask import jsonify
from sqlalchemy import text

from app.services import Session
from . import tasks_survey_bp, logger
from .schema import photo_list_schema

@tasks_survey_bp.route('/boarding/photos/<int:photo_id>', methods=['GET'])
def get_photo_by_id(photo_id):
    """Get a specific photo by ID"""
    current_session = Session()
    
    try:
        # Get photo data
        photo = current_session.execute(
            text("SELECT * FROM tbl_photo_survey_boarding WHERE id_photo = :id"),
            {"id": photo_id}
        )
        
        photo_data = photo_list_schema.dump(photo)
        
        if not photo_data:
            return jsonify({"error": "Photo not found"}), 404
            
        return jsonify(photo_data[0])
    except Exception as e:
        current_session.rollback()
        logger.error(f"Error retrieving photo: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()