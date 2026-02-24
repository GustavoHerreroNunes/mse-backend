import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from dotenv import load_dotenv

# Carrega as variáveis do .env
load_dotenv()

# Lê a URL do banco do .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Cria engine e session
engine = create_engine(DATABASE_URL, echo=False)
Session = scoped_session(sessionmaker(bind=engine))
