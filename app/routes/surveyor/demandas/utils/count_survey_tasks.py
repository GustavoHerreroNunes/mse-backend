from sqlalchemy import text
from .. import logger

def count_survey_tasks(id_demanda, session):
    """Count number of tasks assigned to a specific demanda"""
    try:
        result = session.execute(
            text("SELECT COUNT(*) as task_count FROM tbl_task_survey WHERE id_survey = :id_survey"),
            {"id_survey": id_demanda}
        )
        count = result.fetchone()._mapping["task_count"]
        return count
    except Exception as e:
        logger.error(f"Error counting tasks for demanda {id_demanda}: {str(e)}")
        raise e