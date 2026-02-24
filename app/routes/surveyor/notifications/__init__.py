import logging
from flask import Blueprint

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__) # Não está sendo utilizado?

notifications_bp = Blueprint('notifications-surveyor', __name__, url_prefix="/notifications-surveyor")

@notifications_bp.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
    response.headers.add('Access-Control-Max-Age', '3600')
    return response

# Import routes to register them with the blueprint
from . import create_notification, delete_notification, get_user_notifications
from . import get_user_unread_count, toggle_notification_read_status, options