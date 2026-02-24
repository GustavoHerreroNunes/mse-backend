from sqlalchemy import text
import logging

from services.database import Session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_dados_demanda(demanda_id):
    current_session = Session()
    print('get_dados_demanda')
    try:
        query = """
            SELECT 
                d.cliente, 
                COALESCE(v.vessel_name, '-') AS vessel_name,
                COALESCE(v.vessel_type, '-') AS vessel_type,
                COALESCE(v.country_flag, '-') AS country_flag,
                COALESCE(v.imo_number, '0') AS imo_number,
                COALESCE(TO_CHAR(v.year_of_built, 'YYYY'), '1990') AS year_of_built,
                COALESCE(v.dwt, '0') AS dwt,
                COALESCE(v.vessel_length, '0') AS vessel_length,
                COALESCE(v.vessel_breadth, '0') AS vessel_breadth,
                v.vessel_id,
                CASE 
                    WHEN t.cod_atividade  = '1' THEN 'EMBARK OF CARGO(S)' 
                    WHEN t.cod_atividade  = '2' THEN 'DISCHARGE OF CARGO(S)' 
                    ELSE '-' 
                END AS subject,
                '-' AS title,
                COALESCE(STRING_AGG(c.cargo_name, ', '), '-') AS cargos,
                d.dt_abertura,
                d.nome_demanda,
                COALESCE(d.location, '-') AS location,
                COALESCE(SUM(b.num_bollards_fwd), '0') AS num_bollards_fwd,
                COALESCE(SUM(b.num_bollards_aft), '0') AS num_bollards_aft,
                t.cod_atividade,
                d.id_pasta_gd_demanda,
                d.nome_demanda
            FROM 
                tbl_demandas d
            LEFT JOIN
                tbl_task_survey_boarding b ON b.id_survey = d.id_demanda
            LEFT JOIN 
                tbl_vessel v ON d.id_ship = v.vessel_id
            LEFT JOIN 
                tbl_cargo c ON c.id_task = b.id_task
            LEFT JOIN
                tbl_tarefas t ON t.id_tarefas = b.id_task 
            WHERE 
                d.id_demanda = :demanda_id
            GROUP BY 
                d.cliente, 
                v.vessel_name,
                d.dt_abertura,
                d.nome_demanda,
                d.location,
                v.vessel_type,
                v.country_flag,
                v.imo_number,
                v.year_of_built,
                v.dwt,
                v.vessel_breadth,
                v.vessel_length,
                v.vessel_id,
                t.cod_atividade,
                d.id_pasta_gd_demanda,
                d.nome_demanda;
        """
        
        result = current_session.execute(
            text(query),
            {"demanda_id": demanda_id}
        ).mappings()
        
        row = result.fetchone()
        
        if row is None:
            return None, f"Demanda ID {demanda_id} not found."
        
        data = {
            "cliente": row["cliente"],
            "vessel_name": row["vessel_name"],
            "vessel_type": row["vessel_type"],
            "country_flag": row["country_flag"],
            "imo_number": row["imo_number"],
            "year_of_built": row["year_of_built"],
            "dwt": row["dwt"],
            "vessel_length": row["vessel_length"],
            "vessel_breadth": row["vessel_breadth"],
            "vessel_id": row["vessel_id"],
            "subject": row["subject"],
            "title": row ["title"],
            "cargos": row["cargos"],
            "dt_abertura": row["dt_abertura"],
            "nome_demanda": row["nome_demanda"],
            "location": row["location"],
            "num_bollards_fwd": row["num_bollards_fwd"],
            "num_bollards_aft": row["num_bollards_aft"],
            "cod_atividade": row["cod_atividade"],
            "id_pasta_gd_demanda": row["id_pasta_gd_demanda"],
            "nome_demanda": row["nome_demanda"],
        }
        
        return data, None

    except Exception as e:
        current_session.rollback()
        logger.exception(f"Database error on demanda_id {demanda_id}")
        return None, str(e)
    finally:
        current_session.close()