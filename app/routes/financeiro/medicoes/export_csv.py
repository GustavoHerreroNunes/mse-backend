from flask import jsonify, request, Response
from sqlalchemy import text
from app.services import Session
from . import medicoes_bp, logger
import csv
import io
from datetime import datetime

@medicoes_bp.route('/export_csv', methods=['GET'])
def export_medicoes_csv():
    """Export medições to CSV within a date range"""
    current_session = Session()
    try:
        data = request.args
        data_inicial = data.get("data_inicial")
        data_final = data.get("data_final")

        if not data_inicial or not data_final:
            return jsonify({"error": "Parâmetros 'data_inicial' e 'data_final' são obrigatórios."}), 400

        medicoes = current_session.execute(
            text("""SELECT 
                        m.etl_id, m.id_medicao, d.nome_demanda, m.dt_medicao, m.descricao,
                        m.valor_acordado, m.total_medicao, m.versao, m.status, m.numero, d.tipo_cobranca
                    FROM tbl_medicao m
                    LEFT JOIN tbl_demandas d ON m.id_demanda = d.id_demanda
                    WHERE m.dt_medicao BETWEEN :data_inicial AND :data_final 
                    ORDER BY m.etl_id, m.id_medicao"""),
            {
                "data_inicial": data_inicial,
                "data_final": data_final
            }
        )
        
        rows = medicoes.fetchall()
        
        if not rows:
            return jsonify({"error": "Nenhuma medição encontrada no período especificado."}), 404

        # Create CSV in memory with UTF-8-BOM encoding for Excel
        output = io.StringIO()
        # Add BOM for Excel UTF-8 recognition
        output.write('\ufeff')
        
        # Use semicolon delimiter for Excel (common in Portuguese/European locales)
        writer = csv.writer(output, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        
        # Write header
        writer.writerow([
            'ETL ID', 'ID Medição', 'Nome Demanda', 'Data Medição', 'Descrição',
            'Valor Acordado', 'Total Medição', 'Versão', 'Status', 'Número', 'Tipo Cobrança'
        ])
        
        # Write data rows
        for row in rows:
            writer.writerow([
                row.etl_id,
                row.id_medicao,
                row.nome_demanda or '',
                row.dt_medicao.strftime('%d/%m/%Y') if row.dt_medicao else '',
                row.descricao or '',
                str(row.valor_acordado).replace('.', ',') if row.valor_acordado else '',
                str(row.total_medicao).replace('.', ',') if row.total_medicao else '',
                row.versao or '',
                row.status or '',
                row.numero or '',
                row.tipo_cobranca or ''
            ])
        
        # Prepare response
        output.seek(0)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"medicoes_{data_inicial}_to_{data_final}_{timestamp}.csv"
        
        return Response(
            output.getvalue(),
            mimetype='text/csv; charset=utf-8-sig',
            headers={
                'Content-Disposition': f'attachment; filename={filename}',
                'Access-Control-Expose-Headers': 'Content-Disposition'
            }
        )
        
    except Exception as e:
        current_session.rollback()
        logger.error(f"Erro ao exportar medições para CSV: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()
