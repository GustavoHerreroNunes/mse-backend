from flask import jsonify
from sqlalchemy import text

from app.services import Session
from . import notifications_bp

@notifications_bp.route('/user/<int:user_id>/unread-count', methods=['GET'])
def get_user_unread_count(user_id):
    """Get count of unread notifications for a specific user"""
    current_session = Session()
    
    try:
        result = current_session.execute(
            text("SELECT COUNT(*) as unread_count FROM tbl_notification_surveyor "
                 "WHERE id_user = :id_user AND is_read = FALSE"),
            {
                "id_user": user_id
            }
        )
        
        count = result.fetchone()._mapping["unread_count"]
        return jsonify({"unread_count": count})
    except Exception as e:
        current_session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()