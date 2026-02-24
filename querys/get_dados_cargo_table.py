from sqlalchemy import text
import logging

from services.database import Session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_dados_cargo_table(demanda_id):
    current_session = Session()
    print('get_dados_table')

    try:
        query = """
            SELECT 
                c.cargo_name,
                c.weight,
                c.length,
                c.width,
                c.height,
                c.extra_info,
                c.cargo_type,
                c.cargo_id
            FROM 
                tbl_task_survey_boarding tsb
            JOIN 
                tbl_cargo c ON c.id_task = tsb.id_task
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
                safe(row.get("cargo_name")),
                safe(row.get("weight")),
                safe(row.get("length")),
                safe(row.get("width")),
                safe(row.get("height")),
                safe(row.get("extra_info")),
                safe(row.get("cargo_type")),
                safe(row.get("cargo_id"))
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