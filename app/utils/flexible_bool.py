from marshmallow import fields, ValidationError

class FlexibleBoolean(fields.Boolean):
    """Boolean field that accepts integers (0/1) and converts them to boolean.
    Used for offline support as SQLite 'bool' is actually an integer of two possible
    values (0 or 1)."""
    
    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, int):
            if value in (0, 1):
                return bool(value)
            else:
                raise ValidationError(f"Invalid integer value for boolean field: {value}. Only 0 and 1 are allowed.")
        return super()._deserialize(value, attr, data, **kwargs)