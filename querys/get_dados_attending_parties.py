from sqlalchemy import text
import logging

from services.database import Session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_dados_attending_parties(demanda_id):
    current_session = Session()
    print('get_dados_attending')

    try:
        query = """
            SELECT 
                CONCAT(
                    CASE
                        WHEN asb.gender = 'Feminine' THEN 'Ms.'
                        WHEN asb.gender = 'Masculine' THEN 'Mr.'
                        WHEN asb.gender = 'Other' THEN 'Mx.'
                        ELSE ''
                    END,
                    ' ',
                    asb.attendant_name
                ) AS attendant_name,
                asb.attendant_function,
                asb.behalf
            FROM 
                tbl_task_survey_boarding tsb
            JOIN 
                tbl_attendant_survey_boarding asb ON asb.id_task = tsb.id_task
            WHERE 
                tsb.id_survey = :demanda_id;
        """

        result = current_session.execute(
            text(query),
            {"demanda_id": demanda_id}
        ).mappings()

        rows = result.fetchall()

        if not rows:
            return None, f"Demanda ID {demanda_id} not found."

        # 🟩 Função para tratar nulos e garantir string
        def safe(value):
            return str(value) if value is not None else "-"

        data = [
            [
                safe(row.get("attendant_name")),
                safe(row.get("attendant_function")),
                safe(row.get("behalf"))
            ]
            for row in rows
        ]

        return data, None

    except Exception as e:
        current_session.rollback()
        logger.exception(f"Database error on task_id {demanda_id}")
        return None, str(e)
    finally:
        current_session.close()