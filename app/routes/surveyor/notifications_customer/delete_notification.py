from flask import jsonify
from sqlalchemy import text

from app.services import Session
from . import notifications_customer_bp

@notifications_customer_bp.route('/<int:notification_id>', methods=['DELETE'])
def delete_notification(notification_id):
    """Delete notification by id"""
    current_session = Session()
    
    try:
        # Check if notification exists
        notification = current_session.execute(
            text("SELECT id_notification FROM tbl_notification_customer WHERE id_notification = :id"),
            {"id": notification_id}
        )
        
        if not list(notification):
            return jsonify({"error": "Notification not found"}), 404
        
        current_session.execute(
            text("DELETE FROM tbl_notification_customer WHERE id_notification = :id"),
            {"id": notification_id}
        )
        
        current_session.commit()
        
        return jsonify({"message": "Notification deleted successfully"}), 200
    except Exception as e:
        current_session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()