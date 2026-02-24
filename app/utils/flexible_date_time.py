from marshmallow import fields, ValidationError

class FlexibleDateTime(fields.DateTime):
    """DateTime field that accepts empty strings as null values - needed for FlutterFlow integration."""
    
    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, str):
            if value == '' or value == None or value == 'null':
                return None
        return super()._deserialize(value, attr, data, **kwargs)