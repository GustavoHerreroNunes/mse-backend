from flask import jsonify
from sqlalchemy import text

from app.services import Session
from .schema import notification_list_schema
from . import notifications_customer_bp

# User-based Notification Management
@notifications_customer_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_notifications(user_id):
    """Get all notifications sent to a specific user"""
    current_session = Session()
    
    try:
        notifications = current_session.execute(
            text("""SELECT  
                        nc.message,
                        nc.is_read,
                        nc.created_at,
                        nc.title,
                        nc.id_task,
                        d.nome_demanda,
                        d.id_demanda
                    FROM tbl_notification_customer nc
                    left join tbl_task_survey_boarding sb on sb.id_task = nc.id_task
                    left join tbl_demandas d on d.id_demanda = sb.id_survey 
                    WHERE nc.id_customer = :id_customer 
                    ORDER BY nc.created_at DESC
                """),
            {
                "id_customer": user_id
            }
        )

        current_session.execute(
            text("UPDATE tbl_notification_customer SET is_read = true "
                 "WHERE id_customer = :id_customer"),
            {
                "id_customer": user_id
            }
        )
        current_session.commit()
        
        return notification_list_schema.dumps(notifications), 201
    except Exception as e:
        current_session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()
