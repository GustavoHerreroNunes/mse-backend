from marshmallow import validates, ValidationError
from app import ma
from app.utils.base_schema import BaseSchema

class CustomerSchema(BaseSchema):
    class Meta:
        primary_key = "customer_id"
        fields = (
            "customer_id", "customer_name", "tipo"
        )

    customer_id = ma.Integer(dump_only=True)
    customer_name = ma.String(required=True)
    tipo = ma.String(required=False)

    @validates("customer_name")
    def validate_customer_name(self, value, **kwargs):
        if not value or len(value.strip()) == 0:
            raise ValidationError("Customer name cannot be empty")
        if len(value) > 255:
            raise ValidationError("Customer name cannot exceed 255 characters")

customer_schema = CustomerSchema()
customer_list_schema = CustomerSchema(many=True)