from sqlalchemy import text
import logging

from services.database import Session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_dados_vessel_crane(vessel_id):
    current_session = Session()
    print('get_dados_table')

    try:
        query = """
            SELECT 
                vc.crane_id, 
                sc.swl_capacity_id,
                CASE 
                    WHEN sc.radius_start = 0 THEN NULL 
                    ELSE sc.radius_end 
                END AS radius_end,
                sc.weight
            FROM Tbl_vessel_crane vc
            LEFT JOIN Tbl_swl_capacities sc ON vc.crane_id = sc.crane_id
            WHERE vc.vessel_id = :vessel_id;
        """

        result = current_session.execute(
            text(query),
            {"vessel_id": vessel_id}
        ).mappings()

        rows = result.fetchall()

        if not rows:
            return None, f"Vessel ID {vessel_id} not found."

        # 🟩 Função para tratar nulos e garantir string
        def safe(value):
            return str(value) if value is not None else "-"

        data = [
            [
                safe(row.get("crane_id")),
                safe(row.get("swl_capacity_id")),
                safe(row.get("radius_end")),
                safe(row.get("weight"))
            ]
            for row in rows
        ]

        return data, None

    except Exception as e:
        current_session.rollback()
        logger.exception(f"Database error on vessel_id {vessel_id}")
        return None, str(e)
    finally:
        current_session.close()