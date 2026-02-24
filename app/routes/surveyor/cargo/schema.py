from app import ma
from app.utils.base_schema import BaseSchema
from app.utils.flexible_bool import FlexibleBoolean

class CargoSchema(BaseSchema):
    class Meta:
        primary_key = "cargo_id"
        fields = (
            "cargo_id", "cargo_type", "cargo_name", "weight", "length", "width",
            "height", "extra_info", "id_task", "has_inspection"
        )

    cargo_id = ma.Integer(dump_only=True)
    id_task = ma.Integer(required=True)
    cargo_type = ma.String(required=False)
    cargo_name = ma.String(required=False)
    weight = ma.Float(required=False)
    length = ma.Float(required=False)
    width = ma.Float(required=False)
    height = ma.Float(required=False)
    extra_info = ma.String(required=False)
    has_inspection = FlexibleBoolean(dump_only=True)

cargo_schema = CargoSchema()
cargo_list_schema = CargoSchema(many=True)