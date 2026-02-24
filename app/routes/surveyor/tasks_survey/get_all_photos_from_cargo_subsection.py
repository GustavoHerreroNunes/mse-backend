from flask import jsonify
from sqlalchemy import text

from app.services import Session
from . import tasks_survey_bp, logger
from .schema import photo_list_schema

@tasks_survey_bp.route('/boarding/photos/cargo/<int:id_cargo>/subsection/<int:sub_section_index>', methods=['GET'])
def get_all_photos_from_cargo_section(id_cargo, sub_section_index):
    """Get all photos for a specific cargo"""
    current_session = Session()
    
    try:
        # Check if task exists
        task = current_session.execute(
            text("SELECT cargo_id FROM tbl_cargo WHERE cargo_id = :id"),
            {"id": id_cargo}
        )
        
        if not list(task):
            return jsonify({"error": "Cargo not found"}), 404
            
        # Get all photos for the cargo
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
                WHERE id_cargo = :id_cargo and sub_section_index = :sub_section_index 
                ORDER BY sub_section_index
            """),
            {
                "id_cargo": id_cargo,
                "sub_section_index": sub_section_index
            }
        )
        
        return photo_list_schema.dumps(photos), 200
    except Exception as e:
        current_session.rollback()
        logger.error(f"Error retrieving photos: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()