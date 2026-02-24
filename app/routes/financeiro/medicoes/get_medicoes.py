from flask import jsonify, request
from sqlalchemy import text
from app.services import Session
from . import medicoes_bp
from .schema import medicao_list_schema

@medicoes_bp.route('/', methods=['GET'])
def get_all_medicoes():
    """Get all medicoes"""
    current_session = Session()
    try:
        data = request.args
        data_inicial = data.get("data_inicial")
        data_final = data.get("data_final")

        if not data_inicial or not data_final:
            return jsonify({"error": "Parâmetros 'data_inicial' e 'data_final' são obrigatórios."}), 400

        medicoes = current_session.execute(
            text("""SELECT m.*, d.nome_demanda as ref_mse, d.tipo_cobranca 
                    FROM tbl_medicao m
                    INNER JOIN tbl_demandas d ON m.id_demanda = d.id_demanda
                    WHERE dt_medicao BETWEEN :data_inicial AND :data_final 
                    ORDER BY etl_id"""),
            {
                "data_inicial": data_inicial,
                "data_final": data_final
            }
        )
        return medicao_list_schema.dumps(medicoes)
    except Exception as e:
        current_session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()

@medicoes_bp.route('/demanda/<int:demanda_id>', methods=['GET'])
def get_medicoes_by_demanda(demanda_id):
    """Get all medicoes for a specific demanda"""
    current_session = Session()
    try:
        demanda_check = current_session.execute(
            text("SELECT id_demanda FROM tbl_demandas WHERE id_demanda = :id"),
            {"id": demanda_id}
        )
        if not list(demanda_check):
            return jsonify({"error": "Demanda not found"}), 404

        medicoes = current_session.execute(
            text("SELECT * FROM tbl_medicao WHERE id_demanda = :id_demanda ORDER BY etl_id"),
            {"id_demanda": demanda_id}
        )
        return medicao_list_schema.dumps(medicoes), 200
    except Exception as e:
        current_session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()

@medicoes_bp.route('/by_id/<int:medicao_id>', methods=['GET'])
def get_medicao_by_id(medicao_id):
    """Get a specific medicao by ID"""
    current_session = Session()
    try:
        medicao = current_session.execute(
            text("SELECT * FROM tbl_medicao WHERE id_medicao = :id_medicao"),
            {"id_medicao": medicao_id}
        )
        result = list(medicao)
        if not result:
            return jsonify({"error": "Medicao not found"}), 404
        
        return medicao_list_schema.dumps(result), 200
    except Exception as e:
        current_session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()
