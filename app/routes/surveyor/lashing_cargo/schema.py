from app import ma
from app.utils.base_schema import BaseSchema

class LashingCargoSchema(BaseSchema):
    class Meta:
        primary_key = "cargo_id"
        fields = (
            "cargo_id", "seafastened", "materials", "lines_connected",
            "lines_tighten", "lines_protection", "welded_stoppers",
            "welded_rings", "fitted_stoppers", "structure_failure",
            "approved_crew"
        )

    cargo_id = ma.Integer(required=True)
    seafastened = ma.String(required=False)
    materials = ma.String(required=False)
    lines_connected = ma.String(required=False)
    lines_tighten = ma.String(required=False)
    lines_protection = ma.String(required=False)
    welded_stoppers = ma.String(required=False)
    welded_rings = ma.String(required=False)
    fitted_stoppers = ma.String(required=False)
    structure_failure = ma.String(required=False)
    approved_crew = ma.String(required=False)

lashing_cargo_schema = LashingCargoSchema()
lashing_cargo_list_schema = LashingCargoSchema(many=True)