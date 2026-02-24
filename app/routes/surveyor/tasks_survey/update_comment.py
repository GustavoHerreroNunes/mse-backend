from flask import jsonify, request
from sqlalchemy import text
from marshmallow import ValidationError

from app.services import Session
from . import tasks_survey_bp
from .schema import comment_schema

@tasks_survey_bp.route('/boarding/comments/<int:comment_id>', methods=['PUT'])
def update_comment(comment_id):
    """Update a comment (id_task cannot be changed)"""
    try:
        data = comment_schema.load(request.json, partial=True)
            
        # id_task should not be updated
        if data.get("id_task"):
            return jsonify({"error": "Cannot update id_task field"}), 400
            
        current_session = Session()
        
        try:
            # Check if comment exists
            comment = current_session.execute(
                text("SELECT id_comment FROM tbl_comment_survey_boarding WHERE id_comment = :id"),
                {"id": comment_id}
            )
            
            if not list(comment):
                return jsonify({"error": "Comment not found"}), 404
                
            # Build update query
            update_fields = []
            params = {"id": comment_id}
            
            for field, value in data.items():
                update_fields.append(f"{field} = :{field}")
                params[field] = value
                
            if not update_fields:
                return jsonify({"message": "No fields to update"}), 200
                
            update_query = f"""
                UPDATE tbl_comment_survey_boarding 
                SET {', '.join(update_fields)}
                WHERE id_comment = :id
            """
            
            current_session.execute(text(update_query), params)
            current_session.commit()
            
            return jsonify({"message": "Comment updated successfully"}), 200
        except Exception as e:
            current_session.rollback()
            return jsonify({"error": str(e)}), 500
        finally:
            current_session.close()
    except ValidationError as e:
        return jsonify({"error": "Validation Error.", "details": e.messages})