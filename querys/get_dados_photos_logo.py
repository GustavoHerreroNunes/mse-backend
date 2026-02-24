from sqlalchemy import text
import logging

from services.database import Session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_dados_photos_logo(demanda_id):
    current_session = Session()
    print('get_dados_photos')
    try:
        query = """
            SELECT 
                tpc.url_path
            FROM 
                tbl_photo_client tpc
            JOIN 
                tbl_demandas td ON td.id_client = tpc.id_client
            WHERE 
                td.id_demanda = :demanda_id
        """
        result = current_session.execute(
            text(query),
            {
                "demanda_id": demanda_id,
            }
        ).mappings()
        
        rows = result.fetchall()

        if not rows:
            return None, f"Demanda ID {demanda_id} not found."
        
        # 🟩 Função para tratar nulos e garantir string
        def safe(value):
            return str(value) if value is not None else "-"

        data = [
            [
                safe(row.get("url_path")),
            ]
            for row in rows
        ]

        return data, None

    except Exception as e:
        current_session.rollback()
        logger.exception(f"Database error on demanda_id {demanda_id}")
        return None, str(e)
    finally:
        current_session.close()