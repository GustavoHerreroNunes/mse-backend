import logging
from flask import Blueprint

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

users_surveyor_bp = Blueprint('users_surveyor', __name__, url_prefix="/surveyor/users")

@users_surveyor_bp.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Methods', '*')
    response.headers.add('Access-Control-Max-Age', '3600')
    return response

# Import routes to register them with the blueprint
from . import add_user, delete_user, get_user_by_id, get_users, update_user, options, get_user_by_email
