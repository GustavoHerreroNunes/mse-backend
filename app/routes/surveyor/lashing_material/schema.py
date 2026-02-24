from app import ma
from app.utils.base_schema import BaseSchema
from app.utils.flexible_bool import FlexibleBoolean

class LashingMaterialSchema(BaseSchema):
    class Meta:
        primary_key = "id_lashing_material"
        fields = (
            "id_task", 
            "id_lashing_material", 
            "type", 
            "quantity",
            "weight", 
            "lenght", 
            "id_cargo",
            "has_relation",
            "has_inspection"
        )

    id_task = ma.Integer(required=True)
    id_lashing_material = ma.Integer(dump_only=True)
    type = ma.String(required=False)
    quantity = ma.Integer(required=False)
    weight = ma.Float(required=False)
    lenght = ma.Float(required=False)
    id_cargo = ma.Integer(required=False)
    has_relation = FlexibleBoolean(dump_only=True)
    has_inspection = FlexibleBoolean(dump_only=True)

lashing_material_schema = LashingMaterialSchema()
lashing_material_list_schema = LashingMaterialSchema(many=True)
