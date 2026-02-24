from sqlalchemy import text
import logging

from services.database import Session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_demanda_ids():
    current_session = Session()
    print('get_dados_table')

    try:
        query = """
            SELECT 
                tsp.id_demanda
            FROM tbl_status_pdf tsp
            WHERE tsp.created = FALSE;
        """

        result = current_session.execute(text(query)).mappings()
        rows = result.fetchall()  # ✅ pega todos

        if not rows:
            return None, "Demanda IDs not found."

        # 🟩 Função para tratar nulos e garantir string
        def safe(value):
            return str(value) if value is not None else "-"

        data = []
        for row in rows:
            data.append({"id_demanda": safe(row.get("id_demanda"))})

        return data, None

    except Exception as e:
        current_session.rollback()
        logger.exception("Database error on demanda_id")
        return None, str(e)
    finally:
        current_session.close()
