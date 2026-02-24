from flask import jsonify
from sqlalchemy import text

from app.services import Session
from . import demandas_bp, logger
from .schema import demanda_list_schema
from .utils.count_survey_tasks import count_survey_tasks

@demandas_bp.route('/<int:demanda_id>', methods=['GET'])
def get_demanda_by_id(demanda_id):
    """Get detailed information about a specific demanda by its ID"""
    current_session = Session()
    
    try:
        # Query to get demanda with vessel information
        query = """
            SELECT d.id_demanda, d.nome_demanda, d.survey_status, 
                   d.id_client as client_id, c.customer_name as client_name, 
                   d.id_pasta_gd_demanda, v.vessel_id, v.vessel_name, v.imo_number, 
                   d.dt_entrega as term, d.dt_abertura as opening_date, 
                   d.classificacao as rating, d.location, v.vessel_type,
                   d.moving_to_location
            FROM tbl_demandas d
            LEFT JOIN tbl_vessel v ON d.id_ship = v.vessel_id
			LEFT JOIN tbl_customer c ON d.id_client = c.customer_id
            WHERE d.id_demanda = :demanda_id;

        """
        
        result = current_session.execute(
            text(query),
            {"demanda_id": demanda_id}
        )
        
        demanda_data = demanda_list_schema.dump(result)
        
        if not demanda_data:
            return jsonify({"error": "Demanda not found"}), 404
        
        # Convert to dict and add task count
        demanda_data[0]["tasks_count"] = count_survey_tasks(demanda_id, current_session)

        return jsonify(demanda_data[0])
    except Exception as e:
        current_session.rollback()
        logger.error(f"Error retrieving demanda with ID {demanda_id}: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()