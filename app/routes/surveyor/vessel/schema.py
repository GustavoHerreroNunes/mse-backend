from marshmallow import validates, validates_schema, ValidationError
from app import ma
from app.utils.base_schema import BaseSchema

# Constants from vessel_bp
VALID_VESSEL_TYPES = [
    'Barge', 'Tugboat', 'General Cargo', 'Ro-Ro vessel', 'Container Carrier',
    'Heavy Lifter', 'Pusher Boat', 'Crane Barge', 'Supply Vessel', 'ROV Vessel',
    'Rescue Boat', 'Yatch', 'Passenger Vessel', 'Bulk Carrier']
VALID_CRANE_POSITIONS = ['PS', 'SB', 'AFT', 'FWD', 'PS e AFT', 'PS e FWD', 'SB e AFT', 'SB e FWD']

class SwlCapacitySchema(BaseSchema): #Nenhuma rota está utilizando schema?
    class Meta:
        primary_key = "swl_capacity_id"
        fields = (
            "swl_capacity_id", "crane_id", "weight", 
            "radius_start", "radius_end"
        )
    
    swl_capacity_id = ma.Integer(dump_only=True)
    crane_id = ma.Integer(required=True)
    weight = ma.Float(required=True)
    radius_start = ma.Float(required=True)
    radius_end = ma.Float(required=True)
    
    @validates("weight", "radius_end")
    def validate_positive_values(self, value, **kwargs):
        if value <= 0:
            raise ValidationError("Value must be greater than zero.")
    
    @validates("radius_start")
    def validate_radius_start(self, value, **kwargs):
        if value < 0:
            raise ValidationError("Value must be equal or greater than zero.")

class CraneSchema(BaseSchema):
    class Meta:
        primary_key = "crane_id"
        fields = (
            "crane_id", "vessel_id", "position_on_vessel", 
            "swl_capacities"
        )
    
    crane_id = ma.Integer(dump_only=True)
    vessel_id = ma.Integer(required=True)
    position_on_vessel = ma.String(required=True)
    swl_capacities = ma.List(ma.Nested(SwlCapacitySchema), required=False)
    
    @validates("position_on_vessel")
    def validate_position(self, value, **kwargs):
        if value not in VALID_CRANE_POSITIONS:
            raise ValidationError(f"Invalid crane position '{value}'. Must be one of: {', '.join(VALID_CRANE_POSITIONS)}")

class VesselSchema(BaseSchema):
    class Meta:
        primary_key = "vessel_id"
        fields = (
            "vessel_id", "imo_number", "vessel_name", "vessel_type",
            "vessel_length", "vessel_breadth", "vessel_beam", "vessel_depth",
            "loaded_draft", "light_draft", "gross_tonnage", "bollard_pull",
            "has_crane", "country_flag", "year_of_built", "dwt", "client_id",
            "cranes"
        )
    
    vessel_id = ma.Integer(dump_only=True)
    imo_number = ma.String(allow_none=True)
    vessel_name = ma.String(required=True)
    vessel_type = ma.String(required=True)
    vessel_length = ma.Float(allow_none=True)
    vessel_breadth = ma.Float(allow_none=True)
    vessel_beam = ma.Float(allow_none=True)
    vessel_depth = ma.Float(allow_none=True)
    loaded_draft = ma.Float(allow_none=True)
    light_draft = ma.Float(allow_none=True)
    gross_tonnage = ma.Float(allow_none=True)
    bollard_pull = ma.Float(allow_none=True)
    has_crane = ma.Boolean(allow_none=True)
    country_flag = ma.String(allow_none=True)
    year_of_built = ma.Integer(allow_none=True)
    dwt = ma.Float(allow_none=True)
    client_id = ma.Integer(allow_none=True)
    cranes = ma.List(ma.Nested(CraneSchema), required=False)
    
    @validates("vessel_type")
    def validate_vessel_type(self, value, **kwargs):
        if value not in VALID_VESSEL_TYPES:
            raise ValidationError(f"Invalid vessel type. Must be one of: {', '.join(VALID_VESSEL_TYPES)}")
    
    @validates("vessel_length", "vessel_breadth", "vessel_beam", 
              "vessel_depth", "loaded_draft", "light_draft", "gross_tonnage")
    def validate_positive_values(self, value, **kwargs):
        if value is not None and value <= 0:
            raise ValidationError("Value must be greater than zero.")
        
# Create schema instances
vessel_schema = VesselSchema()
vessel_list_schema = VesselSchema(many=True)
crane_schema = CraneSchema()
crane_list_schema = CraneSchema(many=True)
swl_capacity_schema = SwlCapacitySchema()
swl_capacity_list_schema = SwlCapacitySchema(many=True)