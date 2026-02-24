from flask import jsonify, request
from sqlalchemy import text

from app.services import Session
from . import tarefas_bp, logger
from .schema import tarefas_list_schema

@tarefas_bp.route('/<int:id_demanda>', methods=['GET'])
def get_all_tarefas_demanda(id_demanda):
    """Get all tarefas from a demanda"""
    
    current_session = Session()
    
    try:
        query = ("""
                    SELECT 
                        dt_abertura AT TIME ZONE 'UTC' AT TIME ZONE 'America/Sao_Paulo' AS dt_abertura,
                        atividade,
                        status,
                        demanda,
                        executor,
                        id_tarefas
                    FROM tbl_tarefas d
                    WHERE
                        id_demanda = :id_demanda
                    ORDER BY dt_abertura DESC;
                 """)
        result = current_session.execute(
            text(query),
            {"id_demanda": id_demanda}
        )

        rows = result.fetchall()
        tarefa_data = tarefas_list_schema.dump(rows)

        if not tarefa_data:
            return jsonify({"error": "Nenhuma tarefa encontrada no período especificado."}), 404

        return jsonify(tarefa_data)
    except Exception as e:
        current_session.rollback()
        logger.error(f"Error retrieving tarefas: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()
