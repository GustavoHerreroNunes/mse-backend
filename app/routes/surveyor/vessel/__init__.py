import logging
from flask import Blueprint

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Valid vessel types - add more as needed
VALID_VESSEL_TYPES = ['Barge', 'Tugboat', 'Other']
# Valid crane positions
VALID_CRANE_POSITIONS = ['PS', 'SB', 'AFT', 'FWD', 'PS e AFT', 'PS e FWD', 'SB e AFT', 'SB e FWD']
# Fields for Vessels
FIELDS_FOR_VESSELS = {
    "all": {
        "numeric": [
            'vessel_length', 
            'vessel_breadth', 
            'vessel_beam', 
            'vessel_depth', 
            'loaded_draft', 
            'light_draft', 
            'gross_tonnage', 
            'dwt'
        ],
        "non-numeric": [
            'imo_number',
            'vessel_name',
            'vessel_type',
            'has_crane',
            'country_flag',
            'year_of_built',
            'client_id'
        ]
    },
    "tugboat": {
        "numeric": [
            'bollard_pull' 
        ],
        "non-numeric": []
    },
    "barge": {
        "numeric": [],
        "non-numeric": []
    }
}

vessel_bp = Blueprint('vessel', __name__, url_prefix="/vessels")

@vessel_bp.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Methods', '*')
    response.headers.add('Access-Control-Max-Age', '3600')
    return response

# Import routes to register them with the blueprint
from . import add_vessel, delete_crane, delete_swl_capacity, delete_vessel
from . import get_all_vessels, get_crane_by_id, get_crane_swl_capacities, get_vessel_by_id
from . import get_vessel_cranes, options, search_vessels, update_crane, update_swl_capacity
from . import update_vessel