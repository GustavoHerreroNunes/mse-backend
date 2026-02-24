from app import ma
from app.utils.base_schema import BaseSchema
from app.utils.flexible_bool import FlexibleBoolean

class NotificationsSchema(BaseSchema):
    class Meta:
        primary_key = "id_notification"
        fields = ("id_notification", "id_survey", "id_user", "message",
                  "created_at", "is_read")
    
    id_notification = ma.Integer(dump_only=True)
    id_survey = ma.Integer(required=True)
    id_user = ma.Integer(required=True)
    message = ma.String(required=True)
    created_at = ma.DateTime(dump_only=True)
    is_read = FlexibleBoolean(required=False)
    
notification_schema = NotificationsSchema()
notification_list_schema = NotificationsSchema(many=True)
