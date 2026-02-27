from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from flask import current_app

def get_db_engine():
    db_url = current_app.config['SQLALCHEMY_DATABASE_URI']
    engine = create_engine(
        db_url,
        echo=False,
        # pool_recycle=3600,
        pool_pre_ping=True,
        pool_size=5,        # Max persistent connections per instance
        max_overflow=2      # Extra connections allowed under load
    )
    with engine.connect() as conn:
        print('[JIT]')
        result = conn.execute(text("SHOW jit;")).fetchone()
        print("JIT status:", result[0])  # Should print "off"

    return engine

def get_db_session():
    engine = get_db_engine()
    Session = sessionmaker(bind=engine)
    return Session()

def execute_query(query, params=None):
    session = get_db_session()
    try:
        result = session.execute(query, params)
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()