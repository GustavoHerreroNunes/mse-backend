from flask import jsonify, request
from sqlalchemy import text
from marshmallow import ValidationError

from app.services import Session
from . import tasks_survey_bp
from .schema import comment_schema

# Comments Management
@tasks_survey_bp.route('/boarding/comments', methods=['POST'])
def add_comment():
    """Add a new comment to a task"""
    try:
        data = comment_schema.load(request.json)
        
        current_session = Session()
        
        try:
            # Check if task exists
            task = current_session.execute(
                text("SELECT id_task FROM tbl_task_survey WHERE id_task = :id"),
                {"id": data.get("id_task")}
            )
            
            if not list(task):
                return jsonify({"error": "Task not found"}), 404
                
            # Insert comment
            result = current_session.execute(
                text("""
                    INSERT INTO tbl_comment_survey_boarding (
                        id_task, section_index, sub_section_index, message, 
                        id_cargo, id_lifting_material, id_lashing_material)
                    VALUES (
                        :id_task, :section_index, :sub_section_index, :message, 
                        :id_cargo, :id_lifting_material, :id_lashing_material)
                    RETURNING id_comment
                """),
                {
                    "id_task": data.get("id_task"),
                    "section_index": data.get("section_index"),
                    "sub_section_index": data.get("sub_section_index"),
                    "message": data.get("message"),
                    "id_cargo": data.get("id_cargo"),
                    "id_lifting_material": data.get("id_lifting_material"),
                    "id_lashing_material": data.get("id_lashing_material")
                }
            )
            
            current_session.commit()
            
            comment_id = result.fetchone()._mapping["id_comment"]
            
            return jsonify({
                "message": "Comment added successfully", 
                "id": comment_id
            }), 201
        except Exception as e:
            current_session.rollback()
            return jsonify({"error": str(e)}), 500
        finally:
            current_session.close()
    except ValidationError as e:
        return jsonify({"error": "Validation Error.", "details": e.messages})