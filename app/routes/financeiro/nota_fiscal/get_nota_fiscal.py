from flask import jsonify, request
from sqlalchemy import text
from app.services import Session
from . import nota_fiscal_bp, logger
from .schema import nota_fiscal_list_schema

@nota_fiscal_bp.route('/', methods=['GET'])
def get_all_notas_fiscais():
    """Get all notas fiscais within a date range"""
    current_session = Session()
    try:
        data = request.args
        data_inicial = data.get("data_inicial")
        data_final = data.get("data_final")

        if not data_inicial or not data_final:
            return jsonify({"error": "Parâmetros 'data_inicial' e 'data_final' são obrigatórios."}), 400

        notas_fiscais = current_session.execute(
            text("""SELECT 
                        nf.id_nota, nf.tipo_nota, nf.nota_url, nf.etl_id, nf.numero_nota,
                        nf.dt_emissao, nf.dt_vencimento, nf.valor_bruto, nf.valor_liquido,
                        nf.descricao, nf.valor_real, nf.valor_cotacao, nf.valor_final,
                        nf.dt_pagamento, nf.status,
                        d.nome_demanda, d.cliente, d.classificacao
                    FROM tbl_nota_fiscal nf
                    LEFT JOIN tbl_medicao m ON nf.etl_id = m.etl_id
                    LEFT JOIN tbl_demandas d ON m.id_demanda = d.id_demanda
                    WHERE nf.dt_emissao BETWEEN :data_inicial AND :data_final 
                    ORDER BY nf.etl_id, nf.id_nota"""),
            {
                "data_inicial": data_inicial,
                "data_final": data_final
            }
        )
        return nota_fiscal_list_schema.dumps(notas_fiscais)
    except Exception as e:
        current_session.rollback()
        logger.error(f"Erro ao buscar notas fiscais: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()

@nota_fiscal_bp.route('/by_id/<int:nota_id>', methods=['GET'])
def get_nota_fiscal_by_id(nota_id):
    """Get a specific nota fiscal by ID"""
    current_session = Session()
    try:
        nota_fiscal = current_session.execute(
            text("""SELECT 
                        nf.id_nota, nf.tipo_nota, nf.nota_url, nf.etl_id, nf.numero_nota,
                        nf.dt_emissao, nf.dt_vencimento, nf.valor_bruto, nf.valor_liquido,
                        nf.descricao, nf.valor_real, nf.valor_cotacao, nf.valor_final,
                        nf.dt_pagamento, nf.status,
                        d.nome_demanda, d.cliente, d.classificacao
                    FROM tbl_nota_fiscal nf
                    LEFT JOIN tbl_medicao m ON nf.etl_id = m.etl_id
                    LEFT JOIN tbl_demandas d ON m.id_demanda = d.id_demanda
                    WHERE nf.id_nota = :id_nota"""),
            {"id_nota": nota_id}
        )
        result = list(nota_fiscal)
        if not result:
            return jsonify({"error": "Nota fiscal not found"}), 404
        
        return nota_fiscal_list_schema.dumps(result), 200
    except Exception as e:
        current_session.rollback()
        logger.error(f"Erro ao buscar nota fiscal: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()

@nota_fiscal_bp.route('/by_etl/<int:etl_id>', methods=['GET'])
def get_notas_fiscais_by_etl(etl_id):
    """Get all notas fiscais for a specific ETL ID"""
    current_session = Session()
    try:
        notas_fiscais = current_session.execute(
            text("""SELECT 
                        nf.id_nota, nf.tipo_nota, nf.nota_url, nf.etl_id, nf.numero_nota,
                        nf.dt_emissao, nf.dt_vencimento, nf.valor_bruto, nf.valor_liquido,
                        nf.descricao, nf.valor_real, nf.valor_cotacao, nf.valor_final,
                        nf.dt_pagamento, nf.status,
                        d.nome_demanda, d.cliente, d.classificacao
                    FROM tbl_nota_fiscal nf
                    LEFT JOIN tbl_medicao m ON nf.etl_id = m.etl_id
                    LEFT JOIN tbl_demandas d ON m.id_demanda = d.id_demanda
                    WHERE nf.etl_id = :etl_id 
                    ORDER BY nf.id_nota"""),
            {"etl_id": etl_id}
        )
        result = list(notas_fiscais)
        if not result:
            return jsonify({"error": "Nenhuma nota fiscal encontrada para este ETL ID"}), 404
        
        return nota_fiscal_list_schema.dumps(result), 200
    except Exception as e:
        current_session.rollback()
        logger.error(f"Erro ao buscar notas fiscais por ETL: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()
