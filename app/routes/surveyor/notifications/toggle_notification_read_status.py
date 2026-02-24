from flask import jsonify
from sqlalchemy import text

from app.services import Session
from . import notifications_bp

@notifications_bp.route('/<int:notification_id>/toggle-read', methods=['PUT'])
def toggle_notification_read_status(notification_id):
    """Toggle is_read attribute of a notification"""
    current_session = Session()
    
    try:
        # Check if notification exists
        notification = current_session.execute(
            text("SELECT id_notification, is_read FROM tbl_notification_surveyor WHERE id_notification = :id"),
            {"id": notification_id}
        )
        
        notification_data = notification.fetchone()
        
        if not notification_data:
            return jsonify({"error": "Notification not found"}), 404
            
        new_status = not notification_data._mapping["is_read"]
        
        current_session.execute(
            text("UPDATE tbl_notification_surveyor SET is_read = :is_read "
                 "WHERE id_notification = :id"),
            {
                "id": notification_id,
                "is_read": new_status
            }
        )
        
        current_session.commit()
        
        return jsonify({
            "message": "Notification status updated successfully",
            "is_read": new_status
        }), 200
    except Exception as e:
        current_session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()
