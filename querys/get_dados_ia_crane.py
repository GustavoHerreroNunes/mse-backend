from sqlalchemy import text
import logging

from services.database import Session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_dados_ia_crane(demanda_id):
    current_session = Session()
    print('get_dados_table')

    try:
        query = """
            select 
                tsb.external_cranes,
                tsb.wire,
                tsb.sheaves,
                tsb.operation_condition
            from Tbl_task_survey_boarding tsb
            where tsb.id_survey = :demanda_id
        """

        result = current_session.execute(
            text(query),
            {"demanda_id": demanda_id}
        ).mappings()

        row = result.fetchone()

        if not row:
            return None, f"Demanda ID {demanda_id} not found."

        # 🟩 Função para tratar nulos e garantir string
        def safe(value):
            return str(value) if value is not None else "-"

        data = {
            "external_cranes": safe(row.get("external_cranes")),
            "wire": safe(row.get("wire")),
            "sheaves": safe(row.get("sheaves")),
            "operation_condition": safe(row.get("operation_condition"))
        }

        return data, None

    except Exception as e:
        current_session.rollback()
        logger.exception(f"Database error on demanda_id {demanda_id}")
        return None, str(e)
    finally:
        current_session.close()