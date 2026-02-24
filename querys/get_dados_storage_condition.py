from sqlalchemy import text
import logging

from services.database import Session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_dados_storage_condition(cargo_id):
    current_session = Session()
    print('get_dados_table')

    try:
        query = """
            select 
                tss.proper_stowage,
                tss.obstructions_stowage,
                tss.proper_plating,
                tss.surrounded_risks,
                tss.damages_internal,
                tss.contaminant
            from tbl_step_storage tss
            where tss.cargo_id = :cargo_id
        """
        
        result = current_session.execute(
            text(query),
            {"cargo_id": cargo_id}
        ).mappings()

        rows = result.fetchall()

        if not rows:
            return None, f"Cargo ID {cargo_id} not found."

        # 🟩 Função para tratar nulos e garantir string
        def safe(value):
            return str(value) if value is not None else "-"

        row = rows[0]
        data = {
            "proper_stowage": safe(row.get("proper_stowage")),
            "obstructions_stowage": safe(row.get("obstructions_stowage")),
            "proper_plating": safe(row.get("proper_plating")),
            "surrounded_risks": safe(row.get("surrounded_risks")),
            "damages_internal": safe(row.get("damages_internal")),
            "contaminant": safe(row.get("contaminant"))
        }

        return data, None

    except Exception as e:
        current_session.rollback()
        logger.exception(f"Database error on cargo_id {cargo_id}")
        return None, str(e)
    finally:
        current_session.close()