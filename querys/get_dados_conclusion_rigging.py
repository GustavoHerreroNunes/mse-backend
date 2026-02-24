from sqlalchemy import text
import logging

from services.database import Session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_dados_ia_conclusion_rigging(demanda_id):
    current_session = Session()
    print('get_dados_table')

    try:
        query = """
            SELECT 
                CASE 
                    WHEN COUNT(*) > 0 AND 
                        SUM(
                            CASE 
                                WHEN 
                                    tsr.elements_accordance IN ('Yes', 'Does not apply') AND
                                    tsr.elements_fitted IN ('Yes', 'Does not apply') AND
                                    tsr.safety_devices IN ('Yes', 'Does not apply') AND
                                    tsr.twisted_line IN ('No', 'Does not apply') AND
                                    tsr.slings_contact IN ('No', 'Does not apply') AND
                                    tsr.beginning_inclination IN ('Yes', 'Does not apply') AND
                                    tsr.during_inclination IN ('No', 'Does not apply') AND
                                    tsr.has_pictures_elements IN ('Yes', 'Does not apply') AND
                                    tsr.has_pictures_beginning IN ('Yes', 'Does not apply') AND
                                    tsr.has_pictures_overall IN ('Yes', 'Does not apply') AND
                                    tsr.has_pictures_stowage IN ('Yes', 'Does not apply')
                                THEN 1 
                                ELSE 0 
                            END
                        ) = COUNT(*)
                    THEN 'Good'
                    ELSE 'Bad'
                END AS rigging_condition
            FROM tbl_cargo tc
            LEFT JOIN tbl_step_rigging tsr ON tsr.cargo_id = tc.cargo_id
            LEFT JOIN tbl_task_survey_boarding ttsb 
                ON ttsb.id_task = tc.id_task 
            WHERE ttsb.id_survey = :demanda_id;
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
            "rigging_condition": safe(row.get("rigging_condition"))
        }

        return data, None

    except Exception as e:
        current_session.rollback()
        logger.exception(f"Database error on demanda_id {demanda_id}")
        return None, str(e)
    finally:
        current_session.close()