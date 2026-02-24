from app import ma
from app.utils.base_schema import BaseSchema

class CargoStorageSchema(BaseSchema):
    class Meta:
        primary_key = "cargo_id"
        fields = (
            "cargo_id", "proper_stowage", "obstructions_stowage", "proper_plating",
            "surrounded_risks", "damages_internal", "contaminant"
        )

    cargo_id = ma.Integer(required=True)
    proper_stowage = ma.String(required=False)
    obstructions_stowage = ma.String(required=False)
    proper_plating = ma.String(required=False)
    surrounded_risks = ma.String(required=False)
    damages_internal = ma.String(required=False)
    contaminant = ma.String(required=False)

cargo_storage_schema = CargoStorageSchema()
cargo_storage_list_schema = CargoStorageSchema(many=True)