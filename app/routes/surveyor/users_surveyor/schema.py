from marshmallow import validates, ValidationError
from app import ma
import re
from app.utils.base_schema import BaseSchema

class UserSurveyorSchema(BaseSchema):
    class Meta:
        fields = (
            "id", "display_name", "email", "password", "is_active"
        )

    id = ma.Integer(dump_only=True)
    display_name = ma.String(dump_only=True)
    email = ma.String(required=True)
    password = ma.String(required=True, load_only=True) 
    is_active = ma.Boolean(dump_default=True)
        
    @validates("password")
    def validate_password(self, value, **kwargs):
        if not value:
            return
        
        SpecialSym = ['.', ',', ';', ':', '[', ']', '{', '}', '+', '-', '=', '*', '&', '%', '$', '#', '@', '!', '?', '/']
        if len(value) < 8:
            raise ValidationError("Password must be at least 8 characters long")
        
        if not any(letter in SpecialSym for letter in value):
            raise ValidationError("Password must have at least one special character or symbol like %, $ or #")

user_surveyor_schema = UserSurveyorSchema()
user_surveyor_list_schema = UserSurveyorSchema(many=True)