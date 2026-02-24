from sqlalchemy import text
import logging

from services.database import Session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_dados_lifting_table(demanda_id):
    current_session = Session()
    print('get_dados_table')

    try:
        query = """
            SELECT 
                lm.type,
                lm.quantity,
                lm.weight,
                lm.lenght,
                lm.id_lifting_material
            FROM 
                tbl_task_survey_boarding tsb
            JOIN 
                tbl_lifting_material lm ON lm.id_task = tsb.id_task
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
                safe(row.get("quantity")),
                safe(row.get("type")),
                safe(row.get("weight")),
                safe(row.get("lenght")),
                safe(row.get("id_lifting_material"))
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