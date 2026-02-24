from app import ma
from app.utils.base_schema import BaseSchema
from app.utils.flexible_date_time import FlexibleDateTime
from marshmallow import validates, ValidationError, validates_schema
from sqlalchemy import text
from app.services import Session

VALID_STATUSES = ['Not Started', 'Active', 'Finished']

class StatementOfFactsSchema(BaseSchema):
    class Meta:
        primary_key = "event_id"
        fields = (
            "event_id", "demanda_id", "location", "preliminary_status", "preliminary_timestamp_start",
            "location_status", "location_timestamp_start", "task_status", "task_timestamp_start",
            "ship_status", "ship_timestamp_start", "attendance_status", "attendance_timestamp_start",
            "cargo_status", "cargo_timestamp_start", "preliminary_timestamp_end", "location_timestamp_end",
            "task_timestamp_end", "ship_timestamp_end", "attendance_timestamp_end", "cargo_timestamp_end"
        )

    event_id = ma.Integer(dump_only=True)
    demanda_id = ma.Integer(required=True)
    location = ma.String(required=False, allow_none=True)
    cargo_timestamp_end = FlexibleDateTime(required=False, format='iso', allow_none=True)
    cargo_timestamp_start = FlexibleDateTime(required=False, format='iso', allow_none=True)
    cargo_status = ma.String(required=False)
    attendance_timestamp_end = FlexibleDateTime(required=False, format='iso', allow_none=True)
    attendance_timestamp_start = FlexibleDateTime(required=False, format='iso', allow_none=True)
    attendance_status = ma.String(required=False)
    ship_timestamp_end = FlexibleDateTime(required=False, format='iso', allow_none=True)
    ship_timestamp_start = FlexibleDateTime(required=False, format='iso', allow_none=True)
    ship_status = ma.String(required=False)
    task_timestamp_end = FlexibleDateTime(required=False, format='iso', allow_none=True)
    task_timestamp_start = FlexibleDateTime(required=False, format='iso', allow_none=True)
    task_status = ma.String(required=False)
    location_timestamp_end = FlexibleDateTime(required=False, format='iso', allow_none=True)
    location_timestamp_start = FlexibleDateTime(required=False, format='iso', allow_none=True)
    location_status = ma.String(required=False)
    preliminary_timestamp_end = FlexibleDateTime(required=False, format='iso', allow_none=True)
    preliminary_timestamp_start = FlexibleDateTime(required=False, format='iso', allow_none=True)
    preliminary_status = ma.String(required=False)

    @validates
    def validate_all_status_fields(self, data, **kwargs):
        errors = {}
        for field, value in data.items():
            if field.endswith('_status') and value not in VALID_STATUSES:
                errors[field] = f"Invalid status '{value}'. Valid statuses are {VALID_STATUSES}"
        if errors:
            raise ValidationError(errors)

    @validates_schema
    def validate_all_ids(self, data, **kwargs):
        """Validate all IDs in a single database session"""
        current_session = Session()
        try:
            errors = {}
                        
            # Validate survey_id
            if 'demanda_id' in data:
                result = current_session.execute(
                    text("SELECT id_demanda FROM tbl_demandas WHERE id_demanda = :demanda_id"),
                    {"demanda_id": data['demanda_id']}
                )
                if not result.fetchone():
                    errors['demanda_id'] = f"Invalid demanda_id: '{data['demanda_id']}'. Must exist in tbl_demandas."
                        
            if errors:
                raise ValidationError(errors)
                
        except Exception as e:
            if isinstance(e, ValidationError):
                raise e
            raise ValidationError(f"Error validating IDs: {str(e)}")
        finally:
            current_session.close()

statement_of_facts_schema = StatementOfFactsSchema()
statement_of_facts_list_schema = StatementOfFactsSchema(many=True)

class StatementOfFactsCargoSchema(BaseSchema):
    class Meta:
        primary_key = "event_id"
        fields = (
            "event_id", "cargo_id", "location", "inspection_status", "inspection_timestamp_start",
            "items_status", "items_timestamp_start", "operation_status", "operation_timestamp_start",
            "storage_status", "storage_timestamp_start", "material_status", "material_timestamp_start",
            "board_status", "board_timestamp_start", "inspection_timestamp_end", "items_timestamp_end",
            "operation_timestamp_end", "storage_timestamp_end", "material_timestamp_end", "board_timestamp_end"
        )

    event_id = ma.Integer(dump_only=True)
    cargo_id = ma.Integer(required=True)
    location = ma.String(required=False, allow_none=True)
    board_timestamp_end = FlexibleDateTime(required=False, format='iso', allow_none=True)
    board_timestamp_start = FlexibleDateTime(required=False, format='iso', allow_none=True)
    board_status = ma.String(required=False)
    material_timestamp_end = FlexibleDateTime(required=False, format='iso', allow_none=True)
    material_timestamp_start = FlexibleDateTime(required=False, format='iso', allow_none=True)
    material_status = ma.String(required=False)
    storage_timestamp_end = FlexibleDateTime(required=False, format='iso', allow_none=True)
    storage_timestamp_start = FlexibleDateTime(required=False, format='iso', allow_none=True)
    storage_status = ma.String(required=False)
    operation_timestamp_end = FlexibleDateTime(required=False, format='iso', allow_none=True)
    operation_timestamp_start = FlexibleDateTime(required=False, format='iso', allow_none=True)
    operation_status = ma.String(required=False)
    items_timestamp_end = FlexibleDateTime(required=False, format='iso', allow_none=True)
    items_timestamp_start = FlexibleDateTime(required=False, format='iso', allow_none=True)
    items_status = ma.String(required=False)
    inspection_timestamp_end = FlexibleDateTime(required=False, format='iso', allow_none=True)
    inspection_timestamp_start = FlexibleDateTime(required=False, format='iso', allow_none=True)
    inspection_status = ma.String(required=False)

    @validates
    def validate_all_status_fields(self, data, **kwargs):
        errors = {}
        for field, value in data.items():
            if field.endswith('_status') and value not in VALID_STATUSES:
                errors[field] = f"Invalid status '{value}'. Valid statuses are {VALID_STATUSES}"
        if errors:
            raise ValidationError(errors)

    @validates_schema
    def validate_all_ids(self, data, **kwargs):
        """Validate all IDs in a single database session"""
        current_session = Session()
        try:
            errors = {}
            
            # Validate cargo_id (if provided)
            if 'cargo_id' in data and data['cargo_id'] is not None:
                result = current_session.execute(
                    text("SELECT cargo_id FROM tbl_cargo WHERE cargo_id = :cargo_id"),
                    {"cargo_id": data['cargo_id']}
                )
                if not result.fetchone():
                    errors['cargo_id'] = f"Invalid cargo_id: '{data['cargo_id']}'. Must exist in tbl_cargo."
                        
            if errors:
                raise ValidationError(errors)
                
        except Exception as e:
            if isinstance(e, ValidationError):
                raise e
            raise ValidationError(f"Error validating IDs: {str(e)}")
        finally:
            current_session.close()

statement_of_facts_cargo_schema = StatementOfFactsCargoSchema()
statement_of_facts_cargo_list_schema = StatementOfFactsCargoSchema(many=True)