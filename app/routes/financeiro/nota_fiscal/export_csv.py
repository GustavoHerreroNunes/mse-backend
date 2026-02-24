from flask import jsonify, request, Response
from sqlalchemy import text
from app.services import Session
from . import nota_fiscal_bp, logger
import csv
import io
from datetime import datetime

@nota_fiscal_bp.route('/export_csv', methods=['GET'])
def export_notas_fiscais_csv():
    """Export notas fiscais to CSV within a date range"""
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
        
        rows = notas_fiscais.fetchall()
        
        if not rows:
            return jsonify({"error": "Nenhuma nota fiscal encontrada no período especificado."}), 404

        # Create CSV in memory with UTF-8-BOM encoding for Excel
        output = io.StringIO()
        # Add BOM for Excel UTF-8 recognition
        output.write('\ufeff')
        
        # Use semicolon delimiter for Excel
        writer = csv.writer(output, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        
        # Write header
        writer.writerow([
            'ID Nota', 'Nome Demanda', 'Cliente', 'Classificação', 
            'Tipo Nota', 'Número Nota',
            'Data Emissão', 'Data Vencimento', 'Descrição', 'Valor Bruto', 'Valor Líquido',
            'Valor Dólar', 'Valor Cotação', 'Valor Final',
            'Data Pagamento', 'Status'
        ])
        
        # Write data rows
        for row in rows:
            writer.writerow([
                row.id_nota,
                row.nome_demanda or '',
                row.cliente or '',
                row.classificacao or '',
                row.tipo_nota or '',
                row.numero_nota or '',
                row.dt_emissao.strftime('%d/%m/%Y') if row.dt_emissao else '',
                row.dt_vencimento.strftime('%d/%m/%Y') if row.dt_vencimento else '',
                row.descricao or '',
                str(row.valor_bruto).replace('.', ',') if row.valor_bruto else '',
                str(row.valor_liquido).replace('.', ',') if row.valor_liquido else '',
                str(row.valor_real).replace('.', ',') if row.valor_real else '',
                str(row.valor_cotacao).replace('.', ',') if row.valor_cotacao else '',
                str(row.valor_final).replace('.', ',') if row.valor_final else '',
                row.dt_pagamento.strftime('%d/%m/%Y') if row.dt_pagamento else '',
                row.status or ''
            ])
        
        # Prepare response
        output.seek(0)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"notas_fiscais_{data_inicial}_to_{data_final}_{timestamp}.csv"
        
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
        logger.error(f"Erro ao exportar notas fiscais para CSV: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()
