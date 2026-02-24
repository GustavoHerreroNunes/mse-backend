from marshmallow import validates, ValidationError
from app import ma

class SettingsSchema(ma.Schema):
    class Meta:
        fields = (
            "id_settings", "label_text", "content_value"
        )

    id_settings = ma.String(dump_only=True)
    label_text = ma.String(dump_only=True)
    content_value = ma.String(dump_only=True)
        
settings_schema = SettingsSchema()
settings_list_schema = SettingsSchema(many=True)