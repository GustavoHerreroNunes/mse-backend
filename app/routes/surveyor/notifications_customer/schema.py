from app import ma
from app.utils.base_schema import BaseSchema

class NotificationsCustomerSchema(BaseSchema):
    class Meta:
        primary_key = "id_notification"
        fields = ("id_notification", "id_task", "id_customer", "message",
                  "created_at", "is_read", "title", "id_demanda", "nome_demanda")
    
    id_notification = ma.Integer(dump_only=True)
    id_task = ma.Integer(required=True)
    id_customer = ma.Integer(required=True)
    message = ma.String(required=True)
    created_at = ma.DateTime(dump_only=True)
    is_read = ma.Boolean(required=False)
    title = ma.String(required=True)
    id_demanda = ma.Integer()
    nome_demanda = ma.String()

notification_schema = NotificationsCustomerSchema()
notification_list_schema = NotificationsCustomerSchema(many=True)
