from app import ma

class BaseSchema(ma.Schema):
    class Meta:
        # Define primary_key as a class attribute
        primary_key = "id"
        
    @property
    def pk_field(self):
        """Get the primary key field name"""
        return self.Meta.primary_key