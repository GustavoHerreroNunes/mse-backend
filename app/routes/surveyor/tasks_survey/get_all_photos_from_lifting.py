from flask import jsonify
from sqlalchemy import text

from app.services import Session
from . import tasks_survey_bp, logger
from .schema import photo_list_schema

@tasks_survey_bp.route('/boarding/photos/lifting/<int:id_lifting>', methods=['GET'])
def get_all_photos_from_lifting_section(id_lifting):
    """Get all photos for a specific lifting"""
    current_session = Session()
    
    try:
        # Check if task exists
        task = current_session.execute(
            text("SELECT id_lifting_material FROM tbl_lifting_material WHERE id_lifting_material = :id"),
            {"id": id_lifting}
        )
        
        if not list(task):
            return jsonify({"error": "lifting not found"}), 404
            
        # Get all photos for the lifting
        photos = current_session.execute(
            text("""
                SELECT  
                    id_photo, 
                    id_task, 
                    section_index, 
                    sub_section_index, 
                    id_cargo, 
                    REGEXP_REPLACE(
                        url_path, 
                        '^https://drive\.google\.com/thumbnail\?id=',
                        'https://lh3.googleusercontent.com/d/'
                    ) AS url_path_cliente,
                    id_lifting_material, 
                    id_lashing_material,
                    url_path 
                FROM tbl_photo_survey_boarding 
                WHERE id_lifting_material = :id_lifting
                ORDER BY sub_section_index
            """),
            {
                "id_lifting": id_lifting
            }
        )
        
        return photo_list_schema.dumps(photos), 200
    except Exception as e:
        current_session.rollback()
        logger.error(f"Error retrieving photos: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()