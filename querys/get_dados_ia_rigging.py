from sqlalchemy import text
import logging

from services.database import Session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_dados_ia_rigging(cargo_id):
    current_session = Session()
    print('get_dados_table')

    try:
        query = """
            select 
                tsr.elements_accordance,
                tsr.elements_fitted,
                tsr.safety_devices,
                tsr.twisted_line,
                tsr.slings_contact,
                tsr.beginning_inclination,
                tsr.during_inclination,
                tsr.has_pictures_elements,
                tsr.has_pictures_beginning,
                tsr.has_pictures_overall,
                tsr.has_pictures_stowage
            from tbl_step_rigging tsr
            where cargo_id = :cargo_id
        """

        result = current_session.execute(
            text(query),
            {"cargo_id": cargo_id}
        ).mappings()

        row = result.fetchone()

        if not row:
            return None, f"Cargo ID {cargo_id} not found."

        # 🟩 Função para tratar nulos e garantir string
        def safe(value):
            return str(value) if value is not None else "-"

        data = {
            "elements_accordance": safe(row.get("elements_accordance")),
            "elements_fitted": safe(row.get("elements_fitted")),
            "safety_devices": safe(row.get("safety_devices")),
            "twisted_line": safe(row.get("twisted_line")),
            "slings_contact": safe(row.get("slings_contact")),
            "beginning_inclination": safe(row.get("beginning_inclination")),
            "during_inclination": safe(row.get("during_inclination")),
            "has_pictures_elements": safe(row.get("has_pictures_elements")),
            "has_pictures_beginning": safe(row.get("has_pictures_beginning")),
            "has_pictures_overall": safe(row.get("has_pictures_overall")),
            "has_pictures_stowage": safe(row.get("has_pictures_stowage"))
        }

        return data, None

    except Exception as e:
        current_session.rollback()
        logger.exception(f"Database error on demanda_id {cargo_id}")
        return None, str(e)
    finally:
        current_session.close()