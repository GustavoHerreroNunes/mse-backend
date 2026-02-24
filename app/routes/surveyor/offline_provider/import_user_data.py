import os
import sqlite3
import tempfile
import zlib
from io import BytesIO
from flask import send_file, jsonify, request
from sqlalchemy import text, create_engine, MetaData, Table, Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy.exc import SQLAlchemyError

from app.services import Session, _db_engine
from . import offiline_bp, logger

CARGO_RELATED = [
    'tbl_statement_cargo', 'rlt_lifting_cargo', 'rlt_lashing_cargo',
    'tbl_comment_survey_boarding'
]

LASHING_RELATED = [
    'rlt_lashing_cargo', 'tbl_comment_survey_boarding'
]

LIFTING_RELATED = [
    'rlt_lifting_cargo', 'tbl_comment_survey_boarding'
]

@offiline_bp.route('/test', methods=['GET'])
def test_route():
    return jsonify({"message": "Blueprint is working!"}), 200

def create_sqlite_table_from_postgres(postgres_table, sqlite_conn):
    """Create a SQLite-compatible table from PostgreSQL table structure using raw SQL"""
    
    # Map PostgreSQL types to SQLite types
    type_mapping = {
        'INTEGER': 'INTEGER',
        'VARCHAR': 'TEXT',
        'TEXT': 'TEXT',
        'BOOLEAN': 'INTEGER',
        'DATE': 'TEXT',
        'TIMESTAMP': 'TEXT',
        'NUMERIC': 'REAL',
        'REAL': 'REAL',
        'FLOAT': 'REAL',
        'DOUBLE': 'REAL',
        'DECIMAL': 'REAL'
    }
    
    # Build CREATE TABLE statement
    columns = []
    primary_keys = []
    
    for col in postgres_table.columns:
        # Map column type
        col_type_str = str(col.type)
        sqlite_type = 'TEXT'  # Default fallback
        
        for pg_type, sq_type in type_mapping.items():
            if pg_type in col_type_str.upper():
                sqlite_type = sq_type
                break
        
        # Build column definition
        col_def = f"{col.name} {sqlite_type}"
        
        if col.primary_key:
            primary_keys.append(col.name)
        
        if not col.nullable and not col.primary_key:
            col_def += " NOT NULL"
            
        if col.name == 'last_modified':
            col_def += " DEFAULT CURRENT_TIMESTAMP"

        columns.append(col_def)
    
    # Add sync-related columns to all tables
    columns.extend([
        "is_synced INTEGER",
        "sync_action TEXT DEFAULT 'create'",
        "server_id INTEGER"
    ])

    if(postgres_table.name == 'tbl_photo_survey_boarding'):
        columns.extend([
            "local_photo_path TEXT DEFAULT ''",
            "server_cargo INTEGER",
            "server_lashing INTEGER",
            "server_lifting INTEGER"
        ])

    if(postgres_table.name == 'tbl_comment_survey_boarding'):
        columns.extend([
            "server_cargo INTEGER",
            "server_lashing INTEGER",
            "server_lifting INTEGER"
        ])

    if(postgres_table.name == 'tbl_statement_cargo'):
        columns.extend([
            "server_cargo INTEGER"
        ])

    if(postgres_table.name == 'rlt_lifting_cargo'):
        columns.extend([
            "server_cargo INTEGER",
            "server_lifting INTEGER"
        ])

    if(postgres_table.name == 'rlt_lashing_cargo'):
        columns.extend([
            "server_cargo INTEGER",
            "server_lashing INTEGER",
        ])
    
    # Add primary key constraint if exists
    if primary_keys:
        columns.append(f"PRIMARY KEY ({', '.join(primary_keys)})")
    
    # Create table SQL
    create_sql = f"CREATE TABLE IF NOT EXISTS {postgres_table.name} ({', '.join(columns)})"
    
    # Execute with raw SQL to avoid SQLAlchemy connection issues
    sqlite_conn.execute(create_sql)
    sqlite_conn.commit()


def create_sqlite_triggers(table_name, sqlite_conn):
    trigger_sql = f"""
        CREATE TRIGGER update_{table_name}_timestamp
        BEFORE UPDATE ON {table_name}
        FOR EACH ROW
        WHEN OLD.last_modified = NEW.last_modified
            AND OLD.sync_action != 'create' 
        BEGIN
        UPDATE {table_name}
        SET last_modified = CURRENT_TIMESTAMP,
        sync_action = 'update'
        WHERE rowid = NEW.rowid;
        END;
    """

    sqlite_conn.execute(trigger_sql)
    sqlite_conn.commit()

    print(f"\nTrigger update_{table_name}_timestamp created.\n")

@offiline_bp.route('/user/<int:user_id>/import_user_data', methods=['GET'])
def import_user_data(user_id):
    """Export all user-related data to SQLite database for mobile use"""
    current_session = Session()
    
    try:
        id_demanda = request.args.get("id_demanda", type=int)

        if not id_demanda:
            return jsonify({"error": "Missing required paramenter 'id_demanda'"}), 400

        # First, verify the user exists
        user_check = current_session.execute(
            text("SELECT id FROM tbl_user_surveyor WHERE id = :user_id"),
            {"user_id": user_id}
        ).fetchone()
        
        if not user_check:
            return jsonify({"error": "User not found"}), 404
        
        # Get all related entity IDs in a single optimized query
        entities_query = text("""
            WITH user_entities AS (
                SELECT 
                    d.id_demanda,
                    d.id_ship,
                    d.id_client,
                    t.id_task                    
                FROM tbl_demandas d
                LEFT JOIN tbl_task_survey_boarding t ON d.id_demanda = t.id_survey
                WHERE d.id_surveyor = :user_id AND id_demanda = :id_demanda
            )
            SELECT 
                ue.*,
                st.event_id as st_event_id,
                stc.event_id as stc_event_id,
                at.id_attendant,
                c.cargo_id,
                rlli.id_rlt as rlli_id,
                rlla.id_rlt as rlla_id,
                lm.id_lifting_material,
                lsh.id_lashing_material,
                v.vessel_id,
                vc.crane_id,
                swl.swl_capacity_id,
                p.id_photo,
                cm.id_comment
            FROM user_entities ue
            LEFT JOIN tbl_attendant_survey_boarding at ON ue.id_task = at.id_task  
            LEFT JOIN tbl_statement st ON ue.id_demanda = st.demanda_id
            LEFT JOIN tbl_cargo c ON ue.id_task = c.id_task
            LEFT JOIN tbl_statement_cargo stc ON c.cargo_id = stc.cargo_id
            LEFT JOIN rlt_lifting_cargo rlli ON c.cargo_id = rlli.id_cargo
            LEFT JOIN rlt_lashing_cargo rlla ON c.cargo_id = rlla.id_cargo
            LEFT JOIN tbl_lifting_material lm ON ue.id_task = lm.id_task
            LEFT JOIN tbl_lashing_material lsh ON ue.id_task = lsh.id_task
            LEFT JOIN tbl_vessel v ON ue.id_ship = v.vessel_id
            LEFT JOIN tbl_vessel_crane vc ON v.vessel_id = vc.vessel_id
            LEFT JOIN tbl_swl_capacities swl ON vc.crane_id = swl.crane_id
            LEFT JOIN tbl_customer cus ON ue.id_client = cus.customer_id
            LEFT JOIN tbl_photo_survey_boarding p ON p.id_task = ue.id_task
            LEFT JOIN tbl_comment_survey_boarding cm ON cm.id_task = ue.id_task
        """)
        
        entity_result = current_session.execute(
            entities_query, 
            {"user_id": user_id, "id_demanda": id_demanda}
        ).fetchall()
        
        if not entity_result:
            return jsonify({"error": "No data found for this user"}), 404
        
        # Extract unique IDs for each entity type
        demanda_ids = list(set([row.id_demanda for row in entity_result if row.id_demanda]))
        statement_ids = list(set([row.st_event_id for row in entity_result if row.st_event_id]))
        statement_cargo_ids = list(set([row.stc_event_id for row in entity_result if row.stc_event_id]))
        ship_ids = list(set([row.id_ship for row in entity_result if row.id_ship]))
        task_ids = list(set([row.id_task for row in entity_result if row.id_task]))
        attendants_ids = list(set([row.id_attendant for row in entity_result if row.id_attendant]))
        cargo_ids = list(set([row.cargo_id for row in entity_result if row.cargo_id]))
        cargo_ids = list(set([row.cargo_id for row in entity_result if row.cargo_id]))
        lifting_material_ids = list(set([row.id_lifting_material for row in entity_result if row.id_lifting_material]))
        lashing_material_ids = list(set([row.id_lashing_material for row in entity_result if row.id_lashing_material]))
        vessel_ids = list(set([row.vessel_id for row in entity_result if row.vessel_id]))
        crane_ids = list(set([row.crane_id for row in entity_result if row.crane_id]))
        swl_capacity_ids = list(set([row.swl_capacity_id for row in entity_result if row.swl_capacity_id]))
        photo_ids = list(set([row.id_photo for row in entity_result if row.id_photo]))
        comment_ids = list(set([row.id_comment for row in entity_result if row.id_comment]))
        customer_ids = list(set([row.id_client for row in entity_result if row.id_client]))
        rlt_lifting_ids = list(set([row.rlli_id for row in entity_result if row.rlli_id]))
        rlt_lashing_ids = list(set([row.rlla_id for row in entity_result if row.rlla_id]))
        
        # Create temporary file for SQLite database
        temp_fd, temp_db_path = tempfile.mkstemp(suffix='.db')
        os.close(temp_fd)  # Close the file descriptor immediately
        
        try:
            # Use raw sqlite3 connection for better control
            sqlite_conn = sqlite3.connect(temp_db_path, timeout=30.0)
            sqlite_conn.execute("PRAGMA journal_mode=WAL")  # Use WAL mode to reduce locking
            sqlite_conn.execute("PRAGMA synchronous=NORMAL")  # Faster writes
            
            postgres_metadata = MetaData()
            
            # Define table configurations with their filtering strategies
            table_configs = [
                ('tbl_user_surveyor', 'id', [user_id]),
                ('tbl_demandas', 'id_demanda', demanda_ids),
                ('tbl_statement', 'event_id', statement_ids),
                ('tbl_task_survey_boarding', 'id_task', task_ids),
                ('tbl_attendant_survey_boarding', 'id_attendant', attendants_ids),
                ('tbl_cargo', 'cargo_id', cargo_ids),
                ('rlt_lifting_cargo', 'id_rlt', rlt_lifting_ids),
                ('rlt_lashing_cargo', 'id_rlt', rlt_lashing_ids),
                ('tbl_statement_cargo', 'event_id', statement_cargo_ids),
                ('tbl_lifting_material', 'id_lifting_material', lifting_material_ids),
                ('tbl_lashing_material', 'id_lashing_material', lashing_material_ids),
                ('tbl_vessel', 'vessel_id', vessel_ids),
                ('tbl_vessel_crane', 'crane_id', crane_ids),
                ('tbl_swl_capacities', 'swl_capacity_id', swl_capacity_ids),
                ('tbl_preliminary_checklist', 'id_survey', demanda_ids),
                ('tbl_cargo_condition', 'cargo_id', cargo_ids),
                ('tbl_cargo_condition_wood', 'cargo_id', cargo_ids),
                ('tbl_cargo_condition_reel', 'cargo_id', cargo_ids),
                ('tbl_cargo_condition_bale', 'cargo_id', cargo_ids),
                ('tbl_cargo_condition_thd', 'cargo_id', cargo_ids),
                ('tbl_cargo_condition_machinery', 'cargo_id', cargo_ids),
                ('tbl_cargo_condition_steel', 'cargo_id', cargo_ids),
                ('tbl_cargo_condition_metallic', 'cargo_id', cargo_ids),
                ('tbl_lashing_stopper', 'id_lashing_material', lashing_material_ids),
                ('tbl_lashing_wire', 'id_lashing_material', lashing_material_ids),
                ('tbl_lashing_lines', 'id_lashing_material', lashing_material_ids),
                ('tbl_lashing_shackles', 'id_lashing_material', lashing_material_ids),
                ('tbl_lashing_chain', 'id_lashing_material', lashing_material_ids),
                ('tbl_lashing_tensioner', 'id_lashing_material', lashing_material_ids),
                ('tbl_lifting_wire', 'id_lifting_material', lifting_material_ids),
                ('tbl_lifting_sling', 'id_lifting_material', lifting_material_ids),
                ('tbl_lifting_shackles', 'id_lifting_material', lifting_material_ids),
                ('tbl_lifting_spreader', 'id_lifting_material', lifting_material_ids),
                ('tbl_lifting_chain', 'id_lifting_material', lifting_material_ids),
                ('tbl_lifting_hook', 'id_lifting_material', lifting_material_ids),
                ('tbl_lifting_link', 'id_lifting_material', lifting_material_ids),
                ('tbl_step_storage', 'cargo_id', cargo_ids),
                ('tbl_step_rigging', 'cargo_id', cargo_ids),
                ('tbl_step_lashing', 'cargo_id', cargo_ids),
                ('tbl_notification_surveyor', 'id_user', [user_id]),
                ('tbl_photo_survey_boarding', 'id_photo', photo_ids),
                ('tbl_comment_survey_boarding', 'id_comment', comment_ids),
                ('tbl_customer', 'customer_id', customer_ids),
            ]
            
            total_records = 0
            
            # Process each table
            for table_name, filter_column, filter_ids in table_configs:
                try:                    
                    # Reflect table from PostgreSQL
                    try:
                        postgres_table = Table(table_name, postgres_metadata, autoload_with=_db_engine)
                    except Exception as reflect_error:
                        logger.warning(f"Could not reflect table {table_name}: {str(reflect_error)}")
                        continue
                    
                    # Create SQLite table
                    create_sqlite_table_from_postgres(postgres_table, sqlite_conn)
                    
                    # Build filter condition
                    if len(filter_ids) > 0:
                        if len(filter_ids) == 1:
                            filter_condition = f"{filter_column} = :filter_value"
                            filter_params = {"filter_value": filter_ids[0]}
                        else:
                            placeholders = ','.join([f':id_{i}' for i in range(len(filter_ids))])
                            filter_condition = f"{filter_column} IN ({placeholders})"
                            filter_params = {f'id_{i}': filter_ids[i] for i in range(len(filter_ids))}
                        
                        # Fetch data from PostgreSQL
                        postgres_query = text(f"SELECT * FROM {table_name} WHERE {filter_condition}")
                        data = current_session.execute(postgres_query, filter_params).fetchall()
                    
                        if data:
                            # Get column names from original table
                            original_column_names = [col.name for col in postgres_table.columns]
                            
                            # Add sync columns to the column list
                            all_column_names = original_column_names + ['is_synced', 'sync_action', 'server_id']
                            
                            if table_name in CARGO_RELATED:
                                all_column_names.append('server_cargo')
                            
                            if table_name in LIFTING_RELATED:
                                all_column_names.append('server_lifting')

                            if table_name in LASHING_RELATED:
                                all_column_names.append('server_lashing')

                            # Prepare insert statement
                            placeholders = ', '.join(['?' for _ in all_column_names])
                            insert_sql = f"INSERT INTO {table_name} ({', '.join(all_column_names)}) VALUES ({placeholders})"
                            
                            # Convert data to tuples and add sync values
                            data_tuples = []
                            for row in data:
                                # Get the primary key value for server_id
                                primary_key_value = None
                                for col in postgres_table.columns:
                                    if col.primary_key or (table_name == 'tbl_task_survey_boarding' and col.name == 'id_task') :
                                        primary_key_value = row[original_column_names.index(col.name)]
                                        break
                                
                                # Original row data + sync columns
                                extended_row = list(row) + [1, '', primary_key_value]
                                
                                if table_name in CARGO_RELATED:
                                    if table_name == 'tbl_statement_cargo':
                                        extended_row = extended_row + [row[original_column_names.index('cargo_id')]]
                                    else:
                                        extended_row = extended_row + [row[original_column_names.index('id_cargo')]]
                                
                                if table_name in LIFTING_RELATED:
                                    extended_row = extended_row + [row[original_column_names.index('id_lifting_material')]]

                                if table_name in LASHING_RELATED:
                                    extended_row = extended_row + [row[original_column_names.index('id_lashing_material')]]
                                
                                data_tuples.append(tuple(extended_row))
                            
                            # Insert data using executemany for better performance
                            sqlite_conn.executemany(insert_sql, data_tuples)
                            total_records += len(data_tuples)

                    create_sqlite_triggers(table_name, sqlite_conn)

                    logger.info(f"Exported {len(data) if data else 0} records from {table_name}")
                    
                except Exception as table_error:
                    logger.warning(f"Error processing table {table_name}: {str(table_error)}")
                    continue
            
            # Commit all changes
            sqlite_conn.commit()
            sqlite_conn.close()
            
            if total_records == 0:
                os.unlink(temp_db_path)
                return jsonify({"error": "No data found to export for this user"}), 404
            
            # Create the final database file
            output_filename = f'mse-{user_id}.db'
            output_path = os.path.join(tempfile.gettempdir(), output_filename)
            
            # Remove existing file if it exists
            if os.path.exists(output_path):
                try:
                    os.remove(output_path)
                except OSError:
                    pass  # Ignore if file is still in use
            
            # Copy the SQLite file to the output location
            with open(temp_db_path, 'rb') as src, open(output_path, 'wb') as dst:
                dst.write(src.read())
            
            # Clean up temporary file
            try:
                os.unlink(temp_db_path)
            except OSError:
                pass  # Ignore if temp file is still in use
            
            logger.info(f"Successfully exported {total_records} total records for user {user_id} to {output_filename}")
            
            # Return the file as download
            return send_file(
                output_path,
                as_attachment=True,
                download_name=output_filename,
                mimetype='application/x-sqlite3'
            )
            
        except Exception as sqlite_error:
            # Clean up on error
            try:
                if 'sqlite_conn' in locals():
                    sqlite_conn.close()
                if os.path.exists(temp_db_path):
                    os.unlink(temp_db_path)
            except:
                pass
            raise sqlite_error
            
    except SQLAlchemyError as e:
        current_session.rollback()
        logger.error(f"Database error during export for user {user_id}: {str(e)}")
        return jsonify({"error": "Database error occurred during export"}), 500
    except Exception as e:
        current_session.rollback()
        logger.error(f"Error exporting user data for user {user_id}: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        current_session.close()