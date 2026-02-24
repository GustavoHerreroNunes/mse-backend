from marshmallow import validates, ValidationError, validate
from app import ma
from app.utils.base_schema import BaseSchema

class MedicaoSchema(BaseSchema):
    class Meta:
        primary_key = "etl_id"
        fields = (
            "etl_id", "id_medicao", "id_demanda", "dt_medicao",
            "descricao", "valor_acordado", "total_medicao", "versao",
            "status", "numero", "ref_mse", "tipo_cobranca"
        )

    etl_id = ma.Integer(dump_only=True)
    id_medicao = ma.Integer(required=True)
    id_demanda = ma.Integer(required=True)
    dt_medicao = ma.Date(allow_none=True)
    descricao = ma.String(allow_none=True)
    valor_acordado = ma.Float(allow_none=True)
    total_medicao = ma.Float(allow_none=True)
    versao = ma.Integer(required=True)
    status = ma.String(allow_none=True)
    numero = ma.Integer(allow_none=True)
    ref_mse = ma.String(allow_none=True)
    tipo_cobranca = ma.String(allow_none=True)

    @validates("id_medicao")
    def validate_id_medicao_non_negative(self, value, **kwargs):
        if value is not None and value < 0:
            raise ValidationError("id_medicao cannot be negative.")
    
    @validates("id_demanda")
    def validate_id_demanda_non_negative(self, value, **kwargs):
        if value is not None and value < 0:
            raise ValidationError("id_demanda cannot be negative.")

    @validates("versao")
    def validate_versao_non_negative(self, value, **kwargs):
        if value is not None and value < 0:
            raise ValidationError("versao cannot be negative.")

medicao_schema      = MedicaoSchema()
medicao_list_schema = MedicaoSchema(many=True)