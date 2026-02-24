from sqlalchemy import text
import logging
from services.database import Session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def update_created_status(demanda_id: int, file_url):
    current_session = Session()
    print(f'Atualizando created para demanda_id={demanda_id}')

    try:
        query = """
            UPDATE tbl_status_pdf
            SET created = TRUE,
                modified_at = CURRENT_TIMESTAMP,
                url_path_pdf = :file_url
            WHERE id_demanda = :demanda_id
        """

        result = current_session.execute(
            text(query),
            {"demanda_id": demanda_id, "file_url": file_url}
        )

        current_session.commit()

        # rowcount retorna quantas linhas foram afetadas
        if result.rowcount == 0:
            return False, f"Nenhum registro encontrado para demanda_id {demanda_id}"

        return True, None

    except Exception as e:
        current_session.rollback()
        logger.exception("Erro ao atualizar created")
        return False, str(e)
    finally:
        current_session.close()
