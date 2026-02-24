import logging as log
import google.cloud.logging as logging

logging_client = logging.Client()
logging_client.setup_logging()