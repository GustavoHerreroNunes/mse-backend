import datetime
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import text

from app.services import Session
from .schema import notification_schema
from . import notifications_bp

# Global Notification Management
@notifications_bp.route('/', methods=['POST'])
def create_notification():
    """Create a new notification"""
    try:
        data = notification_schema.load(request.json)
        
        # # Validate required fields
        # required_fields = ["id_survey", "id_user", "message"]
        # for field in required_fields:
        #     if not data.get(field):
        #         return jsonify({"error": f"Request Requirements not met: {field} is required"}), 400
        
        current_session = Session()
        
        try:
            today = datetime.datetime.now()

            result = current_session.execute(
                text("INSERT INTO tbl_notification_surveyor (id_survey, id_user, message, created_at, is_read) "
                    "VALUES (:id_survey, :id_user, :message, :created_at, :is_read) "
                    "RETURNING id_notification"),
                {
                    "id_survey": data.get("id_survey"),
                    "id_user": data.get("id_user"),
                    "message": data.get("message"),
                    "created_at": today,
                    "is_read": False
                }
            )
            
            current_session.commit()
            
            notification_id = result.fetchone()._mapping["id_notification"]
            
            return jsonify({"message": "Notification created successfully", 
                            "id": notification_id}), 201
        except Exception as e:
            current_session.rollback()
            return jsonify({"error": str(e)}), 500
        finally:
            current_session.close()
    except ValidationError as e:
        return jsonify({"error": "Validation Failed.", "details": e.messages}), 400