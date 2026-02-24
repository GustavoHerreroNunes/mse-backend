from .database import get_db_engine
from sqlalchemy.orm import sessionmaker

_db_engine = get_db_engine()
Session = sessionmaker(_db_engine)
