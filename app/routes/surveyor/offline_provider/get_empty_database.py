import os
import sqlite3
import tempfile
import zlib
from io import BytesIO
from flask import send_file, jsonify
from sqlalchemy import text, create_engine, MetaData, Table, Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy.exc import SQLAlchemyError

from app.services import Session, _db_engine
from . import offiline_bp, logger

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

@offiline_bp.route('/get_empty_db', methods=['GET'])
def get_empty_database():
    """Export all empty tables necessary for mobile use"""
    current_session = Session()
    
    try:
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
                ('tbl_user_surveyor', 'id'),
                ('tbl_demandas', 'id_demanda'),                
                ('tbl_task_survey_boarding', 'id_task'),
                ('tbl_attendant_survey_boarding', 'id_attendant'),
                ('tbl_cargo', 'cargo_id'),
                ('tbl_lifting_material', 'id_lifting_material'),
                ('tbl_lashing_material', 'id_lashing_material'),
                ('tbl_vessel', 'vessel_id'),
                ('tbl_vessel_crane', 'crane_id'),
                ('tbl_swl_capacities', 'swl_capacity_id'),
                ('tbl_preliminary_checklist', 'id_survey'),
                ('tbl_cargo_condition_wood', 'cargo_id'),
                ('tbl_cargo_condition_reel', 'cargo_id'),
                ('tbl_cargo_condition_bale', 'cargo_id'),
                ('tbl_cargo_condition_thd', 'cargo_id'),
                ('tbl_cargo_condition_machinery', 'cargo_id'),
                ('tbl_cargo_condition_steel', 'cargo_id'),
                ('tbl_cargo_condition_metallic', 'cargo_id'),
                ('tbl_cargo_condition', 'cargo_id'),
                ('tbl_step_storage', 'cargo_id'),
                ('rlt_lashing_cargo', 'id_cargo'),
                ('tbl_step_rigging', 'cargo_id'),
                ('tbl_step_lashing', 'cargo_id'),
                ('tbl_notification_surveyor', 'id_user',),
                ('tbl_photo_survey_boarding', 'id_photo'),
                ('tbl_customer', 'customer_id'),
            ]
            successful_exports = 0
            
            # Process each table
            for table_name, _ in table_configs:
                try:
                    # Reflect table from PostgreSQL
                    try:
                        postgres_table = Table(table_name, postgres_metadata, autoload_with=_db_engine)
                    except Exception as reflect_error:
                        logger.warning(f"Could not reflect table {table_name}: {str(reflect_error)}")
                        continue
                    
                    # Create SQLite table
                    create_sqlite_table_from_postgres(postgres_table, sqlite_conn)
                    
                    create_sqlite_triggers(table_name, sqlite_conn)

                    successful_exports += 1
                except Exception as table_error:
                    logger.warning(f"Error processing table {table_name}: {str(table_error)}")
                    continue
            logger.info(f"Exported {successful_exports} tables")

            # Commit all changes
            sqlite_conn.commit()
            sqlite_conn.close()
            
            # Create the final database file
            output_filename = f'mse-base.db'
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
            
            logger.info(f"Successfully exported empty database to {output_filename}")
            
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
        logger.error(f"Database error during export: {str(e)}")
        return jsonify({"error": "Database error occurred during export"}), 500
    except Exception as e:
        current_session.rollback()
        logger.error(f"Error exporting tables for database: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        current_session.close()