from marshmallow import validates, ValidationError
from app import ma
import re

class UserCustomerSchema(ma.Schema):
    class Meta:
        fields = (
            "id_user", "display_name", "email", "password", "id_customer"
        )

    id_user = ma.Integer(dump_only=True)
    display_name = ma.String(dump_only=True)
    email = ma.String(required=True)
    password = ma.String(required=True, load_only=True) 
    id_customer = ma.Integer(dump_default=True)
        
    @validates("password")
    def validate_password(self, value, **kwargs):
        if not value:
            return
        
        SpecialSym = ['.', ',', ';', ':', '[', ']', '{', '}', '+', '-', '=', '*', '&', '%', '$', '#', '@', '!', '?', '/']
        if len(value) < 8:
            raise ValidationError("Password must be at least 8 characters long")
        
        if not any(letter in SpecialSym for letter in value):
            raise ValidationError("Password must have at least one special character or symbol like %, $ or #")

user_customer_schema = UserCustomerSchema()
user_customer_list_schema = UserCustomerSchema(many=True)