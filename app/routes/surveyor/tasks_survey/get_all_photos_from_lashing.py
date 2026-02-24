from flask import jsonify
from sqlalchemy import text

from app.services import Session
from . import tasks_survey_bp, logger
from .schema import photo_list_schema

@tasks_survey_bp.route('/boarding/photos/lashing/<int:id_lashing>', methods=['GET'])
def get_all_photos_from_lashing_section(id_lashing):
    """Get all photos for a specific lashing"""
    current_session = Session()
    
    try:
        # Check if task exists
        task = current_session.execute(
            text("SELECT id_lashing_material FROM tbl_lashing_material WHERE id_lashing_material = :id"),
            {"id": id_lashing}
        )
        
        if not list(task):
            return jsonify({"error": "lashing not found"}), 404
            
        # Get all photos for the lashing
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
                    id_lashing_material, 
                    id_lashing_material,
                    url_path 
                FROM tbl_photo_survey_boarding 
                WHERE id_lashing_material = :id_lashing
                ORDER BY sub_section_index
            """),
            {
                "id_lashing": id_lashing
            }
        )
        
        return photo_list_schema.dumps(photos), 200
    except Exception as e:
        current_session.rollback()
        logger.error(f"Error retrieving photos: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()