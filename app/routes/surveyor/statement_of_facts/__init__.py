from flask import Blueprint
import logging

# Configure logger
logger = logging.getLogger(__name__)

# Create blueprint
statement_of_facts_bp = Blueprint(
    'statement_of_facts', 
    __name__, 
    url_prefix='/statement-of-facts'
)

# Import routes
from . import (
    add_statement_of_facts,
    add_statement_of_facts_cargo,
    delete_statement_of_facts,
    delete_statement_of_facts_cargo,
    get_statement_of_facts_by_cargo,
    get_statement_of_facts_by_demanda,
    update_statement_of_facts,
    update_statement_of_facts_cargo,
    options
)
