from flask import request, jsonify
from sqlalchemy import text
from app.services import Session
from . import attendants_survey_bp
from .schema import attendant_survey_schema, attendant_survey_list_schema

@attendants_survey_bp.route('/', methods=['POST'])
def create_attendant():
    """Create a new attendant"""
    data = attendant_survey_schema.load(request.json)
    current_session = Session()
    try:
        result = current_session.execute(
            text("INSERT INTO tbl_attendant_survey_boarding (id_task, attendant_name, attendant_function, gender, behalf) "
                 "VALUES (:id_task, :attendant_name, :attendant_function, :gender, :behalf) "
                 "RETURNING id_attendant"),
            {
                "id_task": data.get("id_task"),
                "attendant_name": data.get("attendant_name"),
                "attendant_function": data.get("attendant_function"),
                "gender": data.get("gender"),
                "behalf": data.get("behalf")
            }
        )
        current_session.commit()
        attendant_id = attendant_survey_list_schema.dump(result)[0].get("id_attendant")
        return jsonify({"message": "Attendant created successfully", "id": attendant_id}), 201
    except Exception as e:
        current_session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()
