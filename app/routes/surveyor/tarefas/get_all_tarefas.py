from flask import jsonify, request
from sqlalchemy import text

from app.services import Session
from . import tarefas_bp, logger
from .schema import tarefas_list_schema

@tarefas_bp.route('/', methods=['GET'])
def get_all_tarefas():
    """Get all tarefas"""
    data = request.args
    data_inicial = data.get("data_inicial")
    data_final = data.get("data_final")

    if not data_inicial or not data_final:
        return jsonify({"error": "Parâmetros 'data_inicial' e 'data_final' são obrigatórios."}), 400
    
    current_session = Session()
    
    try:
        query = ("""
                    SELECT 
                        numero,
                        descricao,
                        nome_tarefa,
                        dt_requisicao AT TIME ZONE 'UTC' AT TIME ZONE 'America/Sao_Paulo' AS dt_requisicao,
                        dt_abertura AT TIME ZONE 'UTC' AT TIME ZONE 'America/Sao_Paulo' AS dt_abertura,
                        horas_estimadas,
                        atividade,
                        cod_atividade,
                        cliente,
                        prioridade,
                        status,
                        tipo,
                        demanda,
                        dt_finalizacao AT TIME ZONE 'UTC' AT TIME ZONE 'America/Sao_Paulo' AS dt_finalizacao,
                        dt_prazo AT TIME ZONE 'UTC' AT TIME ZONE 'America/Sao_Paulo' AS dt_prazo,
                        nome_demanda,
                        executor,
                        comentario_exec,
                        revisor,
                        comentario_revisor,
                        classificacao,
                        comentado_por,
                        dt_comentario_extra AT TIME ZONE 'UTC' AT TIME ZONE 'America/Sao_Paulo' AS dt_comentario_extra,
                        comentario_extra,
                        dt_comentario_exec_rev AT TIME ZONE 'UTC' AT TIME ZONE 'America/Sao_Paulo' AS dt_comentario_exec_rev,
                        comentado_por_extra,
                        dt_coment_validacao AT TIME ZONE 'UTC' AT TIME ZONE 'America/Sao_Paulo' AS dt_coment_validacao,
                        coment_por_validacao,
                        coment_validacao,
                        created_time AT TIME ZONE 'UTC' AT TIME ZONE 'America/Sao_Paulo' AS created_time,
                        hh_total,
                        aprovada_por,
                        id_pasta_tarefa,
                        custo_indicativo,
                        custo_total,
                        document_type,
                        service_type,
                        sequential_number,
                        document_review,
                        id_tarefas
                    FROM tbl_tarefas d
                    WHERE
                        dt_abertura BETWEEN :data_inicial AND :data_final
                    ORDER BY dt_abertura DESC;
                 """)
        result = current_session.execute(
            text(query),
            {"data_inicial": data_inicial, "data_final": data_final}
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