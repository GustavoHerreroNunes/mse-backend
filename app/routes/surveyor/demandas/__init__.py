import logging
from flask import Blueprint

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

demandas_bp = Blueprint("demandas", __name__, url_prefix="/demandas")

@demandas_bp.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, OPTIONS')
    response.headers.add('Access-Control-Max-Age', '3600')
    return response

# Import routes to register them with the blueprint
from . import get_demanda_by_id, get_demandas_by_user, get_all_tasks_from_survey, get_demanda_by_date
from . import update_demanda_status, search_demanda_tarefas, options, update_demanda_location, get_demandas_by_customer
from . import update_demanda_moving