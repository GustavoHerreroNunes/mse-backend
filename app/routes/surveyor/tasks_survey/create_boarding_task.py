from flask import request, jsonify
from sqlalchemy import text
from marshmallow import ValidationError

from app.services import Session
from . import tasks_survey_bp, logger
from .schema import task_survey_schema

# Boarding Tasks Management
@tasks_survey_bp.route('/boarding', methods=['POST'])
def create_boarding_task():
    """Create a new boarding task"""
    try:
        data = task_survey_schema.load(request.json)
           
        current_session = Session()
        
        try:
            # Insert into boarding task table
            result = current_session.execute(
                text("""
                    INSERT INTO tbl_task_survey_boarding (
                        id_survey, id_user, task_title, task_description, 
                        finished, last_task_done, num_bollards_fwd, num_bollards_aft, 
                        finished_mark_one, finished_mark_two, finished_mark_three
                    ) 
                    VALUES (
                        :id_survey, :id_user, :task_title, :task_description, 
                        false, -1, 0, 0, 
                        false, false, false
                    ) 
                    RETURNING id_task
                """),
                {
                    "id_survey": data.get("id_survey"),
                    "id_user": data.get("id_user"),
                    "task_title": data.get("task_title"),
                    "task_description": data.get("task_description")
                }
            )
            
            current_session.commit()
            
            task_id = result.fetchone()._mapping["id_task"]
            
            return jsonify({
                "message": "Boarding task created successfully", 
                "id": task_id
            }), 201
        except Exception as e:
            current_session.rollback()
            logger.error(f"Error creating boarding task: {str(e)}")
            return jsonify({"error": str(e)}), 500
        finally:
            current_session.close()
    except ValidationError as e:
        return jsonify({"error": "Validation error", "details": e.messages}), 400