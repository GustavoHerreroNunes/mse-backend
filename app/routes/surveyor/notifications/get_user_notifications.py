from flask import jsonify
from sqlalchemy import text

from app.services import Session
from .schema import notification_list_schema
from . import notifications_bp

# User-based Notification Management
@notifications_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_notifications(user_id):
    """Get all notifications sent to a specific user"""
    current_session = Session()
    
    try:
        notifications = current_session.execute(
            text("SELECT * FROM tbl_notification_surveyor WHERE id_user = :id_user "
                 "ORDER BY created_at DESC"),
            {
                "id_user": user_id
            }
        )
        
        return notification_list_schema.dumps(notifications), 201
    except Exception as e:
        current_session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()
