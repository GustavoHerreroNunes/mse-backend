from app import ma
from app.utils.base_schema import BaseSchema

class PhotoClientSchema(BaseSchema):
    class Meta:
        primary_key = "id_photo"
        fields = ("id_photo", "id_client", "url_path")

    id_photo = ma.Integer(dump_only=True)
    id_client = ma.Integer(required=True)
    url_path = ma.String(required=True)

photo_client_schema = PhotoClientSchema()
photo_client_list_schema = PhotoClientSchema(many=True)
