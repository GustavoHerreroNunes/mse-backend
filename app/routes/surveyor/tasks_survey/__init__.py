import logging
from flask import Blueprint

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

tasks_survey_bp = Blueprint('tasks-survey', __name__, url_prefix="/tasks-survey")

@tasks_survey_bp.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Methods', '*')
    response.headers.add('Access-Control-Max-Age', '3600')
    return response

# Import routes to register them with the blueprint
from . import add_comment, add_photo, create_boarding_task
from . import delete_boarding_task, delete_photo, get_all_comments_from_task
from . import get_all_photos_from_task, get_boarding_task_by_id, get_comment_by_id
from . import get_photo_by_id, options, update_boarding_task
from . import update_vessel_conditions, update_bollards, update_storage_adq
from . import update_comment, update_photo, get_all_info_task
from . import get_all_photos_from_task_section, get_all_photos_from_cargo_subsection
from . import get_all_photos_from_task_sub_section, get_comments_from_task_sub_section
from . import get_comments_from_cargo_subsection, get_comments_from_lifting_subsection
from . import get_comments_from_lashing_subsection, get_comments_from_task_section
from . import delete_comment, get_all_photos_from_lifting, get_all_photos_from_lashing