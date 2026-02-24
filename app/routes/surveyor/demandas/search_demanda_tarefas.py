from flask import jsonify, request
from sqlalchemy import text

from app.services import Session
from . import demandas_bp, logger

@demandas_bp.route('/tarefas', methods=['GET'])
def search_demanda_tarefas():
    """Search for tarefas matching the name provided"""

    search_parameter = request.args.get("name")

    if not search_parameter:
        return jsonify({"error": "Missing required query parameter 'name'"}), 400

    current_session = Session()
    
    try:        
        tasks = current_session.execute(
            text("""
                 SELECT nome_tarefa FROM tbl_tarefas WHERE LOWER(nome_tarefa) LIKE LOWER(:search)
            """),
            {"search": f"%{search_parameter}%"}
        )

        logger.info(tasks)
        result = [dict(row)["nome_tarefa"] for row in tasks.mappings()]
        
        return jsonify(result), 200
    except Exception as e:
        current_session.rollback()
        logger.error(f"Error retrieving tarefas for name '{search_parameter}': {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()