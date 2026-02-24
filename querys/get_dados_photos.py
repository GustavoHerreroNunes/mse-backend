from sqlalchemy import text
import logging

from services.database import Session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_dados_photos(demanda_id, index, sub_index, cargo_id = None, id_lifting_material = None):
    current_session = Session()
    print('get_dados_photos')
    try:
        print(cargo_id)
        if cargo_id:
            query = """
                SELECT 
                    p.url_path
                FROM 
                    tbl_task_survey_boarding tsb
                JOIN 
                    tbl_photo_survey_boarding p ON p.id_task = tsb.id_task
                WHERE 
                    tsb.id_survey = :demanda_id
                    AND p.section_index = :index
                    AND p.sub_section_index = :sub_index
                    AND p.id_cargo = :cargo_id;
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
                    p.url_path
                FROM 
                    tbl_task_survey_boarding tsb
                JOIN 
                    tbl_photo_survey_boarding p ON p.id_task = tsb.id_task
                WHERE 
                    tsb.id_survey = :demanda_id
                    AND p.section_index = :index
                    AND p.sub_section_index = :sub_index
                    AND p.id_lifting_material = :id_lifting_material;
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
                    p.url_path
                FROM 
                    tbl_task_survey_boarding tsb
                JOIN 
                    tbl_photo_survey_boarding p ON p.id_task = tsb.id_task
                WHERE 
                    tsb.id_survey = :demanda_id
                    AND p.section_index = :index
                    AND p.sub_section_index = :sub_index;
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