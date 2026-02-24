from sqlalchemy import text
import logging

from services.database import Session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_dados_comments(demanda_id, index, sub_index, cargo_id = None, id_lifting_material = None):
    current_session = Session()
    print('get_dados_comments')
    try:   
        if cargo_id:
            query = """
                SELECT 
                    COALESCE(c.message, '-') AS message
                FROM 
                    tbl_task_survey_boarding tsb
                JOIN 
                    tbl_comment_survey_boarding c ON c.id_task = tsb.id_task
                WHERE 
                    tsb.id_survey = :demanda_id
                    AND c.section_index = :index
                    AND c.sub_section_index = :sub_index
                    AND c.id_cargo = :cargo_id
            """
            result = current_session.execute(
                text(query),
                {
                    "demanda_id": demanda_id,
                    "index": index,
                    "sub_index": sub_index,
                    "cargo_id": cargo_id
                }
            ).mappings()
        elif id_lifting_material:
            query = """
                SELECT 
                    COALESCE(c.message, '-') AS message
                FROM 
                    tbl_task_survey_boarding tsb
                JOIN 
                    tbl_comment_survey_boarding c ON c.id_task = tsb.id_task
                WHERE 
                    tsb.id_survey = :demanda_id
                    AND c.section_index = :index
                    AND c.sub_section_index = :sub_index
                    AND c.id_lifting_material = :id_lifting_material
            """
            result = current_session.execute(
                text(query),
                {
                    "demanda_id": demanda_id,
                    "index": index,
                    "sub_index": sub_index,
                    "id_lifting_material": id_lifting_material
                }
            ).mappings()
        else:
            query = """
                SELECT 
                    COALESCE(c.message, '-') AS message
                FROM 
                    tbl_task_survey_boarding tsb
                JOIN 
                    tbl_comment_survey_boarding c ON c.id_task = tsb.id_task
                WHERE 
                    tsb.id_survey = :demanda_id
                    AND c.section_index = :index
                    AND c.sub_section_index = :sub_index;
            """
        
            result = current_session.execute(
                text(query),
                {
                    "demanda_id": demanda_id,
                    "index": index,
                    "sub_index": sub_index
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
                safe(row.get("message")),
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