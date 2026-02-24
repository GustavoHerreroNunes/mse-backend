from app import ma
from app.utils.base_schema import BaseSchema

class LiftingOperationSchema(BaseSchema):
    class Meta:
        primary_key = "cargo_id"
        fields = (
            "cargo_id", "elements_accordance", "elements_fitted", "safety_devices",
            "twisted_line", "slings_contact", "beginning_inclination", "during_inclination",
            "has_pictures_elements", "has_pictures_beginning", "has_pictures_overall", "has_pictures_stowage"
        )

    cargo_id = ma.Integer(required=True)
    elements_accordance = ma.String(required=False)
    elements_fitted = ma.String(required=False)
    safety_devices = ma.String(required=False)
    twisted_line = ma.String(required=False)
    slings_contact = ma.String(required=False)
    beginning_inclination = ma.String(required=False)
    during_inclination = ma.String(required=False)
    has_pictures_elements = ma.String(required=False)
    has_pictures_beginning = ma.String(required=False)
    has_pictures_overall = ma.String(required=False)
    has_pictures_stowage = ma.String(required=False)

lifting_operation_schema = LiftingOperationSchema()
lifting_operation_list_schema = LiftingOperationSchema(many=True)