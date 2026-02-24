from app import ma
from app.utils.base_schema import BaseSchema

class CargoConditionSchema(BaseSchema):
    class Meta:
        primary_key = "cargo_id"
        fields = (
            "cargo_id", "well_received", "instruction",
            "external_condition", "packing", "identification_condition",
            "protection", "stability", "cleanliness", "integrity",
            "warning_labels", "markings", "moisture", "weight_distribution",
            "stacking", "shifting"
        )

    cargo_id = ma.Integer(required=True)
    well_received = ma.String(required=False)
    instruction = ma.String(required=False)
    external_condition = ma.String(required=False)
    packing = ma.String(required=False)
    identification_condition = ma.String(required=False)
    protection = ma.String(required=False)
    stability = ma.String(required=False)
    cleanliness = ma.String(required=False)
    integrity = ma.String(required=False)
    warning_labels = ma.String(required=False)
    markings = ma.String(required=False)
    moisture = ma.String(required=False)
    weight_distribution = ma.String(required=False)
    stacking = ma.String(required=False)
    shifting = ma.String(required=False)

cargo_condition_schema = CargoConditionSchema()
cargo_condition_list_schema = CargoConditionSchema(many=True)