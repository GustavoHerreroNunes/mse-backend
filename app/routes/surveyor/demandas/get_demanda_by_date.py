from flask import jsonify, request
from sqlalchemy import text

from app.services import Session
from . import demandas_bp, logger
from .schema import demanda_list_schema

@demandas_bp.route('/', methods=['GET'])
def get_demandas_by_period():
    """Get all demandas within a given opening date range"""
    data = request.args
    data_inicial = data.get("data_inicial")
    data_final = data.get("data_final")

    if not data_inicial or not data_final:
        return jsonify({"error": "Parâmetros 'data_inicial' e 'data_final' são obrigatórios."}), 400

    current_session = Session()
    
    try:
        query = """
            SELECT 
                executor,
                numero,
                conclusao,
                tipo,
                prioridade,
                status,
                horas_estimadas,
                dt_entrega AT TIME ZONE 'UTC' AT TIME ZONE 'America/Sao_Paulo' AS dt_entrega,
                dt_finalizacao AT TIME ZONE 'UTC' AT TIME ZONE 'America/Sao_Paulo' AS dt_finalizacao,
                nome_demanda,
                cliente,
                dt_abertura AT TIME ZONE 'UTC' AT TIME ZONE 'America/Sao_Paulo' AS dt_abertura,
                dt_requisicao AT TIME ZONE 'UTC' AT TIME ZONE 'America/Sao_Paulo' AS dt_requisicao,
                classificacao,
                descricao,
                id_pasta_gd_demanda,
                id_pasta_gd_cliente,
                criador,
                custo_indicativo,
                custo_total,
                informacoes_adicionais,
                customer_name,
                ship_name,
                imo_number,
                location,
                survey_status,
                have_arrived,
                time_confimation AT TIME ZONE 'UTC' AT TIME ZONE 'America/Sao_Paulo' AS time_confimation,
                location_confirmation,
                id_ship,
                id_demanda,
                id_surveyor,
                id_client,
                surveyor_email,
                valor_acordado,
                hora_extra,
                tipo_cobranca
            FROM tbl_demandas d
            WHERE
                dt_abertura BETWEEN :data_inicial AND :data_final
            ORDER BY dt_abertura DESC;
        """

        result = current_session.execute(
            text(query),
            {"data_inicial": data_inicial, "data_final": data_final}
        )

        rows = result.fetchall()
        demanda_data = demanda_list_schema.dump(rows)

        if not demanda_data:
            return jsonify({"error": "Nenhuma demanda encontrada no período especificado."}), 404

        return jsonify(demanda_data)
    
    except Exception as e:
        current_session.rollback()
        logger.error(f"Erro ao buscar demandas: {str(e)}")
        return jsonify({"error": str(e)}), 500

    finally:
        current_session.close()