from marshmallow import validates, ValidationError, validate
from app import ma
from app.utils.base_schema import BaseSchema

class AttendantSurveySchema(BaseSchema):
    class Meta:
        primary_key = "id_attendant"
        fields = (
            "id_attendant", "id_task", "attendant_name",
            "attendant_function", "gender", "behalf"
        )

    id_attendant = ma.Integer(dump_only=True)
    id_task = ma.Integer(required=True)
    attendant_name = ma.String(required=True)
    attendant_function = ma.String(required=True)
    gender = ma.String(required=True)
    behalf = ma.String(required=True)

    @validates("id_task")
    def validate_non_negative(self, value, **kwargs):
        if value is not None and value < 0:
            raise ValidationError("Value cannot be negative.")

attendant_survey_schema      = AttendantSurveySchema()
attendant_survey_list_schema = AttendantSurveySchema(many=True)