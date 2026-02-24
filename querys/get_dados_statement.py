from sqlalchemy import text
import logging

from services.database import Session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_dados_statement(demanda_id):
    current_session = Session()
    print('get_dados_table')

    try:
        query = """
            SELECT 
                event_id,
                demanda_id,
                location,
                CASE 
                    WHEN preliminary_status = 'Finished' THEN 'Preliminary Check-list'
                    ELSE NULL
                END AS preliminary_status,
                preliminary_timestamp_start,
                CASE 
                    WHEN location_status = 'Finished' THEN 'Arrival of Surveyor'
                    ELSE NULL
                END AS location_status,
                location_timestamp_start,
                CASE 
                    WHEN task_status = 'Finished' THEN 'Start Survey'
                    ELSE NULL
                END AS task_status,
                task_timestamp_start,
                CASE 
                    WHEN attendance_status = 'Finished' THEN 'Safety Meeting'
                    ELSE NULL
                END AS attendance_status,
                attendance_timestamp_start,
                CASE 
                    WHEN cargo_status = 'Finished' THEN 'Cargo'
                    ELSE NULL
                END AS cargo_status,
                cargo_timestamp_start,
                preliminary_timestamp_end,
                location_timestamp_end,
                task_timestamp_end,
                attendance_timestamp_end,
                cargo_timestamp_end 
            FROM tbl_statement
            WHERE demanda_id = :demanda_id;
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
            "event_id": safe(row.get("event_id")),
            "demanda_id": safe(row.get("demanda_id")),
            "location": safe(row.get("location")),
            "preliminary_status": safe(row.get("preliminary_status")),
            "preliminary_timestamp_start": safe(row.get("preliminary_timestamp_start")),
            "location_status": safe(row.get("location_status")),
            "location_timestamp_start": safe(row.get("location_timestamp_start")),
            "task_status": safe(row.get("task_status")),
            "task_timestamp_start": safe(row.get("task_timestamp_start")),
            "attendance_status": safe(row.get("attendance_status")),
            "attendance_timestamp_start": safe(row.get("attendance_timestamp_start")),
            "cargo_status": safe(row.get("cargo_status")),
            "cargo_timestamp_start": safe(row.get("cargo_timestamp_start")),
            "preliminary_timestamp_end": safe(row.get("preliminary_timestamp_end")),
            "location_timestamp_end": safe(row.get("location_timestamp_end")),
            "task_timestamp_end": safe(row.get("task_timestamp_end")),
            "attendance_timestamp_end": safe(row.get("attendance_timestamp_end")),
            "cargo_timestamp_end": safe(row.get("cargo_timestamp_end")),
        }

        return data, None

    except Exception as e:
        current_session.rollback()
        logger.exception(f"Database error on demanda_id {demanda_id}")
        return None, str(e)
    finally:
        current_session.close()