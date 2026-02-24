from app import ma
from app.utils.base_schema import BaseSchema
from marshmallow import fields

class RelationSchema(BaseSchema):
    class Meta:
        primary_key = "id_rlt"
        fields = (
            "id_cargo", "id_lashing_material", "id_lifting_material", "id_rlt"
        )

    id_cargo = ma.Integer(required=True)

    # Agora aceitam lista de inteiros
    id_lashing_material = fields.List(fields.Integer(), required=False)
    id_lifting_material = fields.List(fields.Integer(), required=False)

    id_rlt = ma.Integer(required=False)

class RelationOfflineLiftingSchema(BaseSchema):
    class Meta:
        primary_key = "id_rlt"
        fields = (
            "id_cargo", "id_lifting_material", "id_rlt"
        )

    id_cargo = ma.Integer(required=True)

    id_lifting_material = ma.Integer(required=False)

    id_rlt = ma.Integer(dump_only=True)

class RelationOfflineLashingSchema(BaseSchema):
    class Meta:
        primary_key = "id_rlt"
        fields = (
            "id_cargo", "id_lashing_material", "id_rlt"
        )

    id_cargo = ma.Integer(required=True)

    id_lashing_material = ma.Integer(required=False)

    id_rlt = ma.Integer(dump_only=True)


relation_schema = RelationSchema()
relation_list_schema = RelationSchema(many=True)
relation_off_lifting_schema = RelationOfflineLiftingSchema()
relation_off_lashing_schema = RelationOfflineLashingSchema()
