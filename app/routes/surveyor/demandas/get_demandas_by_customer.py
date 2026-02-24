from flask import jsonify, request
from sqlalchemy import text
from datetime import date
from marshmallow import ValidationError

from app.services import Session
from . import demandas_bp, logger
from .schema import demanda_schema, demanda_list_schema
from .utils.count_survey_tasks import count_survey_tasks

@demandas_bp.route('/surveyor/customer/<int:customer_id>', methods=['GET'])
def get_demandas_by_customer(customer_id):
    """Get all demandas assigned to a specific survey user id with optional filters:
    - Multiple status values (comma separated)
    - forToday parameter to show only demandas due today
    """
    # Get status filter(s) - supports ?status=A,B,C format
    status_filters = []
    if request.args.get('status'):
        # Handle comma-separated values
        status_values = request.args.get('status').split(',')
        status_filters.extend([s.strip() for s in status_values if s.strip()])
    
    # Get forToday parameter
    for_today = request.args.get('forToday', 'false').lower() == 'true'
    
    current_session = Session()
    
    try:
        # Build base query
        query = """
            SELECT d.id_demanda, d.nome_demanda, d.survey_status, 
                d.id_client, c.customer_name, s.display_name,
                d.id_pasta_gd_demanda, v.vessel_id, v.vessel_name, v.imo_number, 
                d.dt_entrega as term, d.dt_abertura as opening_date, 
                d.classificacao, d.location, v.vessel_type,
                d.have_arrived, d.time_confimation, d.location_confirmation
            FROM tbl_demandas d
            LEFT JOIN tbl_vessel v ON d.id_ship = v.vessel_id
            LEFT JOIN tbl_customer c ON d.id_client = c.customer_id
            left join tbl_user_surveyor s on s.id = d.id_surveyor
            WHERE d.id_client = :customer_id
            AND d.tipo = 'OPERAÇÕES'
        """
        
        params = {"customer_id": customer_id}
        
        # Apply status filters if provided
        if status_filters:
            # Validate each status filter
            for status in status_filters:
                demanda_schema.load({"survey_status": status}, partial=True)
            
            placeholders = [f":status_{i}" for i in range(len(status_filters))]
            query += f" AND d.survey_status IN ({', '.join(placeholders)})"
            
            for i, status in enumerate(status_filters):
                params[f"status_{i}"] = status
            
        result = current_session.execute(text(query), params)
        
        demandas = demanda_list_schema.dump(result)
        for row in demandas:
            row["tasks_count"] = count_survey_tasks(row["id_demanda"], current_session)
            
        return jsonify(demandas)
    except ValidationError as e:
        return jsonify({"error": "Validation Error", "details": e.messages}), 400
    except Exception as e:
        current_session.rollback()
        logger.error(f"Error retrieving demandas: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()