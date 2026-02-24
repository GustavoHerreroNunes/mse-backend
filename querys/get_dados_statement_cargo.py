from sqlalchemy import text
import logging

from services.database import Session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_dados_statement_cargo(cargo_id):
    current_session = Session()
    print('get_dados_table')

    try:
        query = """
            SELECT 
                event_id,
                cargo_id,
                location,
                CASE 
                    WHEN inspection_status = 'Finished' THEN 'Cargo inspection'
                    ELSE NULL
                END AS inspection_status,
                inspection_timestamp_start,
                CASE 
                    WHEN items_status = 'Finished' THEN 'Lifting items'
                    ELSE NULL
                END AS items_status,
                items_timestamp_start,
                CASE 
                    WHEN operation_status = 'Finished' THEN 'Lifting operation'
                    ELSE NULL
                END AS operation_status,
                operation_timestamp_start,
                CASE 
                    WHEN storage_status = 'Finished' THEN 'Cargo storage on board'
                    ELSE NULL
                END AS storage_status,
                storage_timestamp_start,
                CASE 
                    WHEN material_status = 'Finished' THEN 'Lashing material'
                    ELSE NULL
                END AS material_status,
                material_timestamp_start,
                CASE 
                    WHEN board_status = 'Finished' THEN 'Lashing cargo on board'
                    ELSE NULL
                END AS board_status,
                board_timestamp_start,
                inspection_timestamp_end,
                items_timestamp_end,
                operation_timestamp_end,
                storage_timestamp_end,
                material_timestamp_end,
                board_timestamp_end
            FROM tbl_statement_cargo
            WHERE cargo_id = :cargo_id;
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
            "event_id": safe(row.get("event_id")),
            "cargo_id": safe(row.get("cargo_id")),
            "location": safe(row.get("location")),
            "inspection_status": safe(row.get("inspection_status")),
            "inspection_timestamp_start": safe(row.get("inspection_timestamp_start")),
            "items_status": safe(row.get("items_status")),
            "items_timestamp_start": safe(row.get("items_timestamp_start")),
            "operation_status": safe(row.get("operation_status")),
            "operation_timestamp_start": safe(row.get("operation_timestamp_start")),
            "storage_status": safe(row.get("storage_status")),
            "storage_timestamp_start": safe(row.get("storage_timestamp_start")),
            "material_status": safe(row.get("material_status")),
            "material_timestamp_start": safe(row.get("material_timestamp_start")),
            "board_status": safe(row.get("board_status")),
            "board_timestamp_start": safe(row.get("board_timestamp_start")),
            "inspection_timestamp_end": safe(row.get("inspection_timestamp_end")),
            "items_timestamp_end": safe(row.get("items_timestamp_end")),
            "operation_timestamp_end": safe(row.get("operation_timestamp_end")),
            "storage_timestamp_end": safe(row.get("storage_timestamp_end")),
            "material_timestamp_end": safe(row.get("material_timestamp_end")),
            "board_timestamp_end": safe(row.get("board_timestamp_end")),
        }

        return data, None

    except Exception as e:
        current_session.rollback()
        logger.exception(f"Database error on cargo_id {cargo_id}")
        return None, str(e)
    finally:
        current_session.close()