from datetime import datetime
from flask import jsonify, request
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from ....utils.log_util import log

from app.services import Session
from . import offiline_bp
from ..users_surveyor.schema import user_surveyor_schema
from ..demandas.schema import demanda_schema
from ..tasks_survey.schema import task_survey_schema
from ..cargo.schema import cargo_schema
from ..lifting_material.schema import lifting_material_schema
from ..lashing_material.schema import lashing_material_schema
from ..vessel.schema import vessel_schema, swl_capacity_schema, crane_schema
from ..preliminary_checklist.schema import checklist_schema
from ..cargo_condition.schema import cargo_condition_schema
from ..cargo_storage.schema import cargo_storage_schema
from ..lifting_operation.schema import lifting_operation_schema
from ..lashing_cargo.schema import lashing_cargo_schema
from ..notifications.schema import notification_schema
from ..attendants_survey.schema import attendant_survey_schema
from ..cargo_inspection.schema import (
    cargo_wood_schema, cargo_bale_schema, cargo_machinery_schema,
    cargo_metallic_schema, cargo_reel_schema, cargo_steel_schema,
    cargo_thd_schema
)
from ..lifting_inspection.schema import (
    lifting_chain_schema, lifting_hook_schema, lifting_link_schema,
    lifting_shackles_schema, lifting_sling_schema, lifting_spreader_schema,
    lifting_wire_schema
)
from ..lashing_inspection.schema import (
    lashing_chain_schema, lashing_lines_schema, lashing_shackles_schema,
    lashing_stopper_schema, lashing_tensioner_schema, lashing_wire_schema
)
from ..statement_of_facts.schema import (
    statement_of_facts_cargo_schema, statement_of_facts_schema
)
from ..relations.schema import (
    relation_off_lifting_schema,
    relation_off_lashing_schema
)
from ..tasks_survey.schema import comment_schema

SCHEMA_MAPPING = {
    'tbl_user_surveyor': user_surveyor_schema,
    'tbl_demandas': demanda_schema,
    'tbl_attendant_survey_boarding': attendant_survey_schema,
    'tbl_task_survey_boarding': task_survey_schema,
    'tbl_cargo': cargo_schema,
    'tbl_lifting_material': lifting_material_schema,
    'tbl_lashing_material': lashing_material_schema,
    'tbl_vessel': vessel_schema,
    'tbl_vessel_crane': crane_schema,
    'tbl_swl_capacities': swl_capacity_schema,
    'tbl_preliminary_checklist': checklist_schema,
    'tbl_cargo_condition': cargo_condition_schema,
    'tbl_cargo_condition_wood': cargo_wood_schema,
    'tbl_cargo_condition_reel': cargo_reel_schema,
    'tbl_cargo_condition_bale': cargo_bale_schema,
    'tbl_cargo_condition_thd': cargo_thd_schema,
    'tbl_cargo_condition_machinery': cargo_machinery_schema,
    'tbl_cargo_condition_steel': cargo_steel_schema,
    'tbl_cargo_condition_metallic': cargo_metallic_schema,
    "tbl_lashing_stopper": lashing_stopper_schema,
    "tbl_lashing_wire": lashing_wire_schema,
    "tbl_lashing_lines": lashing_lines_schema,
    "tbl_lashing_shackles": lashing_shackles_schema,
    "tbl_lashing_chain": lashing_chain_schema,
    "tbl_lashing_tensioner": lashing_tensioner_schema,
    "tbl_lifting_wire": lifting_wire_schema,
    "tbl_lifting_sling": lifting_sling_schema,
    "tbl_lifting_shackles": lifting_shackles_schema,
    "tbl_lifting_spreader": lifting_spreader_schema,
    "tbl_lifting_chain": lifting_chain_schema,
    "tbl_lifting_hook": lifting_hook_schema,
    "tbl_lifting_link": lifting_link_schema,
    'tbl_statement': statement_of_facts_schema,
    'tbl_statement_cargo': statement_of_facts_cargo_schema,
    'tbl_step_storage': cargo_storage_schema,
    'tbl_step_rigging': lifting_operation_schema,
    'tbl_step_lashing': lashing_cargo_schema,
    'tbl_notification_surveyor': notification_schema,
    'rlt_lifting_cargo': relation_off_lifting_schema,
    'rlt_lashing_cargo': relation_off_lashing_schema,
    'tbl_comment_survey_boarding': comment_schema
}

CARGO_DEPENDENT = [
    'tbl_cargo_condition', 'tbl_step_storage', 'tbl_step_rigging', 'tbl_cargo_condition_wood',
    'tbl_cargo_condition_reel', 'tbl_cargo_condition_bale', 'tbl_cargo_condition_thd',
    'tbl_cargo_condition_machinery', 'tbl_cargo_condition_steel', 'tbl_cargo_condition_metallic',
    'tbl_step_lashing'
]

LIFTING_DEPENDENT = [
    "tbl_lifting_wire", "tbl_lifting_sling", "tbl_lifting_shackles", 
    "tbl_lifting_chain", "tbl_lifting_hook", "tbl_lifting_link",
    "tbl_lifting_spreader"
]

LASHING_DEPENDENT = [
    "tbl_lashing_stopper", "tbl_lashing_wire", "tbl_lashing_lines",
    "tbl_lashing_shackles", "tbl_lashing_chain", "tbl_lashing_tensioner"
]

# Map of all cargo, lifting and lashing Local and Server ids created at this run
_cargoLocal2ServerMap: dict = {}
_liftingLocal2ServerMap: dict = {}
_lashingLocal2ServerMap: dict = {}

def _addCargoId(localId, serverId):
    print(f"Added {localId}: {serverId}")
    _cargoLocal2ServerMap[localId] = serverId

def _addLiftingId(localId, serverId):
    print(f"Added {localId}: {serverId}")
    _liftingLocal2ServerMap[localId] = serverId

def _addLashingId(localId, serverId):
    print(f"Added {localId}: {serverId}")
    _lashingLocal2ServerMap[localId] = serverId

def _getServerId(localId, type):
    if type == 'cargo':
        print(f"Get {localId}: {_cargoLocal2ServerMap[localId]}")
        return _cargoLocal2ServerMap[localId]
    if type == 'lifting':
        print(f"Get {localId}: {_liftingLocal2ServerMap[localId]}")
        return _liftingLocal2ServerMap[localId]
    if type == 'lashing':
        print(f"Get {localId}: {_lashingLocal2ServerMap[localId]}")
        return _lashingLocal2ServerMap[localId]
    return -1

def create_row(data, local_id, server_id, server_cargo, server_lifting, server_lashing, pk_field, table, schema, dump_only_fields, session, result):
    # Check if server_id exists and verify if record already exists in database
    if server_id is not None and server_id != 0:
        verify_query = text(
            f"SELECT {pk_field}, last_modified FROM {table} WHERE {pk_field} = :pk_value"
        )
        existing_record = session.execute(verify_query, {'pk_value': server_id})
        
        if existing_record.rowcount > 0:
            # Record exists, call update_row instead
            log.info(f"[create_row] Record with server_id {server_id} already exists in {table}. Calling update_row.")
            record_data = existing_record.fetchone()
            timestamp = record_data[1].strftime('%Y-%m-%d %H:%M:%S') if record_data[1] else None
            
            update_row(
                data, local_id, server_id, server_cargo,
                server_lifting, server_lashing, timestamp,
                pk_field, table, schema, dump_only_fields,
                session, result
            )
            return result
    
    data_for_validation = data

    # Remove read-only fields
    for field in dump_only_fields:
        data_for_validation.pop(field, None)

    if table == 'tbl_statement_cargo':
        if server_cargo is not None and server_cargo != 0:
            data_for_validation['cargo_id'] = server_cargo
        else:
            correct_id = _getServerId(data_for_validation['cargo_id'], 'cargo')
            data_for_validation['cargo_id'] = correct_id

    if table == 'rlt_lifting_cargo' or table == 'rlt_lashing_cargo':
        if server_cargo is not None and server_cargo != 0:
            data_for_validation['id_cargo'] = server_cargo
        else:
            correct_id = _getServerId(data_for_validation['id_cargo'], 'cargo')
            data_for_validation['id_cargo'] = correct_id

    if table == 'rlt_lifting_cargo':
        if server_lifting is not None and server_lifting != 0:
            data_for_validation['id_lifting_material'] = server_lifting
        else:
            correct_id = _getServerId(data_for_validation['id_lifting_material'], 'lifting')
            data_for_validation['id_lifting_material'] = correct_id

    if table == 'rlt_lashing_cargo':
        if server_lashing is not None and server_lashing != 0:
            data_for_validation['id_lashing_material'] = server_lashing
        else:
            correct_id = _getServerId(data_for_validation['id_lashing_material'], 'lashing')
            data_for_validation['id_lashing_material'] = correct_id

    if table == 'tbl_comment_survey_boarding':
        if server_cargo is not None and server_cargo != 0 and server_cargo != 'null':
            data_for_validation['id_cargo'] = server_cargo
            log.info('[comment] server cargo ok')
        elif data_for_validation['id_cargo'] is not None and data_for_validation['id_cargo'] != 0 and data_for_validation['id_cargo'] != 'null':
            correct_id = _getServerId(data_for_validation['id_cargo'], 'cargo')
            data_for_validation['id_cargo'] = correct_id
            log.info('[comment] server cargo None, getting local data')
        else:
            data_for_validation.pop('id_cargo')
            log.info('[comment] server cargo None, popping it')

        if server_lifting is not None and server_lifting != 0:
            data_for_validation['id_lifting_material'] = server_lifting
        elif data_for_validation['id_lifting_material'] is not None and data_for_validation['id_lifting_material'] != 0:
            correct_id = _getServerId(data_for_validation['id_lifting_material'], 'lifting')
            data_for_validation['id_lifting_material'] = correct_id
        else:
            data_for_validation.pop('id_lifting_material')

        if server_lashing is not None and server_lashing != 0:
            data_for_validation['id_lashing_material'] = server_lashing
        elif data_for_validation['id_lashing_material'] is not None and data_for_validation['id_lashing_material'] != 0:
            correct_id = _getServerId(data_for_validation['id_lashing_material'], 'lashing')
            data_for_validation['id_lashing_material'] = correct_id
        else:
            data_for_validation.pop('id_lashing_material')
            
    validated_data = schema.load(data_for_validation)

    if table in CARGO_DEPENDENT:
        if server_id is not None and server_id != 0:
            validated_data[pk_field] = server_id
        else:
            correct_id = _getServerId(local_id, 'cargo')
            validated_data[pk_field] = correct_id

    if table in LIFTING_DEPENDENT:
        if server_id is not None and server_id != 0:
            validated_data[pk_field] = server_id
        else:
            correct_id = _getServerId(local_id, 'lifting')
            validated_data[pk_field] = correct_id

    if table in LASHING_DEPENDENT:
        if server_id is not None and server_id != 0:
            validated_data[pk_field] = server_id
        else:
            correct_id = _getServerId(local_id, 'lashing')
            validated_data[pk_field] = correct_id
    
    # Build INSERT query with dynamic PK field
    columns = ', '.join(validated_data.keys())
    values = ', '.join([f":{key}" for key in validated_data.keys()])
    query = text(
        f"INSERT INTO {table} ({columns}) "
        f"VALUES ({values}) "
        f"RETURNING {pk_field}"  # Dynamic PK field
    )
    
    result_set = session.execute(query, validated_data)
    new_id = result_set.fetchone()[0]
    session.commit()

    if table == 'tbl_cargo':
        _addCargoId(local_id, new_id)

    if table == 'tbl_lifting_material':
        _addLiftingId(local_id, new_id)

    if table == 'tbl_lashing_material':
        _addLashingId(local_id, new_id)
    
    result["status"] = "success"
    result["server_id"] = new_id

    return result

def update_row(data, local_id, server_id, server_cargo, server_lifting, server_lashing, timestamp, pk_field, table, schema, dump_only_fields, session, result):
    if not server_id:
        log.error(f"[export_data_user] Missing server ID for update")
        result["error"] = "Missing server ID for update"
        return 

    result['server_id'] = server_id

    local_timestamp = timestamp
    if not local_timestamp:
        log.error(f"[export_data_user] Missing timestamp for update")
        result["error"] = "Missing timestamp for update"
        return 

    local_timestamp = datetime.strptime(local_timestamp, '%Y-%m-%d %H:%M:%S')

    data_for_validation = data

    # pk_value
    data_for_validation.pop(pk_field, None)

    # Remove read-only fields
    for field in dump_only_fields:
        data_for_validation.pop(field, None)

    validated_data = schema.load(data_for_validation, partial=True)

    verify_conflict_query = text(
        f"SELECT last_modified FROM {table} WHERE {pk_field} = :pk_value"
    )

    result_conflict = session.execute(
        verify_conflict_query,
        {
            'pk_value': server_id
        }
    )

    # If there're no rows with such server_id, then creates a new one to avoid data loses
    # PS: There're two of these conditionals because the function is not atomic, so between
    # one line and other, the row could be deleted
    if result_conflict.rowcount == 0:
        result["error"] = "Record not found. Created a new one to preserve data integrity."
        create_row(
            data, local_id, server_id, server_cargo,
            server_lifting, server_lashing, pk_field,
            table, schema, dump_only_fields, 
            session, result
        )

    else:
        cloud_timestamp = result_conflict.fetchone()[0]
        if local_timestamp <= cloud_timestamp:
            result["status"] = 'conflict'
            result['error'] = 'Cloud server have a newer version of this record.'
        else:
    
            # Build UPDATE query with dynamic PK field
            set_clauses = ', '.join([f"{key} = :{key}" for key in validated_data.keys()])
            query = text(
                f"UPDATE {table} SET {set_clauses} "
                f"WHERE {pk_field} = :pk_value "
                f"RETURNING {pk_field}"
            )
            validated_data['pk_value'] = server_id
            
            result_set = session.execute(query, validated_data)

            # If there're no rows with such server_id, then creates a new one to avoid data loses
            # PS: There're two of these conditionals because the function is not atomic, so between
            # one line and other, the row could be deleted
            if result_set.rowcount == 0:
                result["error"] = "Record not found. Created a new one to preserve data integrity."
                create_row(
                    data, local_id, server_id, server_cargo, 
                    server_lifting, server_lashing, pk_field, 
                    table, schema, dump_only_fields, 
                    session, result
                )
            else:
                result["status"] = "success"
            session.commit()

def delete_row(server_id, pk_field, table, session, result):
    if not server_id:
        result["error"] = "Missing server ID for delete"
        return result
    
    query = text(
        f"DELETE FROM {table} "
        f"WHERE {pk_field} = :pk_value "
        f"RETURNING {pk_field}"
    )
    
    session.execute(query, {'pk_value': server_id})
    
    result["status"] = "success"
    result["server_id"] = server_id
    session.commit()

    return result

@offiline_bp.route('/export_user_data', methods=['POST'])
def export_user_data():
    try:
        log.info('[export_user_data] Starting proccess')
        data = request.get_json()
        if not data or 'operations' not in data:
            log.error('[export_user_data] Invalid payload')
            return jsonify({"error": "Invalid payload format"}), 400
            
        operations = data.get('operations', [])
        if(len(operations) <= 0):
            return([]), 200

        results = []
        session = Session()

        log.info(operations)

        for op in operations:
            result = {
                "status": "failed",
                "action": op.get('action', 'unknown'),
                "table": op.get('table', 'unknown'),
                "server_id": None,
                "local_id": op.get('local_id')
            }
            
            try:
                table = op['table']
                action = op.get('action')
                
                if table not in SCHEMA_MAPPING:
                    result["error"] = f"Table {table} not configured"
                    results.append(result)
                    continue
                    
                schema = SCHEMA_MAPPING[table]
                pk_field = schema.pk_field  # Get primary key field name
                
                dump_only_fields = [
                    name
                    for name, field in schema.fields.items()
                    if field.dump_only
                ]

                # Handle CREATE operation
                if action == 'create':
                    create_row(
                        op.get('data'), op.get('local_id'), op.get('server_id'),
                        op.get('server_cargo'), op.get('server_lifting'), op.get('server_lashing'), 
                        pk_field, table, schema, 
                        dump_only_fields, session, result
                    )
                
                # Handle UPDATE operation
                elif action == 'update':
                    update_row(
                        op.get('data'), op.get('local_id'), op.get('server_id'),
                        op.get('server_cargo'), op.get('server_lifting'), op.get('server_lashing'), 
                        op.get('timestamp'), pk_field, table, 
                        schema, dump_only_fields, session, result
                    )
                    
                # Handle DELETE operation
                elif action == 'delete':
                    delete_row(
                        op.get('server_id'), pk_field, table,
                        session, result
                    )
                
                else:
                    result["error"] = f"Invalid action: {action}"
                
                results.append(result)
            
            except ValidationError as e:
                session.rollback()
                result["error"] = f"Validation error: {e.messages}"
                log.error(f"[export_user_data] Validatio error {e.messages}")
                results.append(result)
            except SQLAlchemyError as e:
                session.rollback()
                result["error"] = f"Database error: {str(e)}"
                log.error(f"[export_user_data] Validatio error {str(e)}")
                results.append(result)
            except Exception as e:
                session.rollback()
                result["error"] = f"Processing error: {str(e)}"
                log.error(f"[export_user_data] Validatio error {str(e)}")
                results.append(result)
        
        log.info(result)
        return jsonify(results)
        
    except Exception as e:
        log.error('[export_user_data] System error')
        log.error(str(e))
        return jsonify({"error": f"System error: {str(e)}"}), 500