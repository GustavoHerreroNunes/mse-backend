from flask import jsonify
from . import health_bp
from app.services.database import get_db_engine
from sqlalchemy.orm import sessionmaker
import time

@health_bp.route('/ping', methods=['GET'])
def ping():
    start = time.time()
    new_engine = get_db_engine()
    Session = sessionmaker(new_engine)
    Session()
    end = time.time()
    duration = end - start
    print(f"Engine creation: {duration}")
    return jsonify({"duration": duration})