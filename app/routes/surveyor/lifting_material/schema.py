from app import ma
from app.utils.base_schema import BaseSchema
from app.utils.flexible_bool import FlexibleBoolean

class LiftingMaterialSchema(BaseSchema):
    class Meta:
        primary_key = "id_lifting_material"
        fields = (
            "id_task", "id_lifting_material", "type", "quantity",
            "weight", "lenght", "id_cargo", "has_relation", "has_inspection"
        )

    id_task = ma.Integer(required=True)
    id_lifting_material = ma.Integer(dump_only=True)
    type = ma.String(required=False)
    quantity = ma.Integer(required=False)
    weight = ma.Float(required=False)
    lenght = ma.Float(required=False)
    id_cargo = ma.Integer(required=False)
    has_relation = FlexibleBoolean(dump_only=True)
    has_inspection = FlexibleBoolean(dump_only=True)

lifting_material_schema = LiftingMaterialSchema()
lifting_material_list_schema = LiftingMaterialSchema(many=True)