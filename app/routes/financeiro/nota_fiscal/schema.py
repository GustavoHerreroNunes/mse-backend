from marshmallow import validates, ValidationError
from app import ma
from app.utils.base_schema import BaseSchema

class NotaFiscalSchema(BaseSchema):
    class Meta:
        primary_key = "id_nota"
        fields = (
            "id_nota", "tipo_nota", "nota_url", "etl_id", "numero_nota",
            "dt_emissao", "dt_vencimento", "valor_bruto", "valor_liquido",
            "descricao", "valor_real", "valor_cotacao", "valor_final",
            "dt_pagamento", "status", "nome_demanda", "cliente", "classificacao"
        )

    id_nota = ma.Integer(dump_only=True)
    tipo_nota = ma.String(allow_none=True, validate=lambda x: len(x) <= 10 if x else True)
    nota_url = ma.String(allow_none=True)
    etl_id = ma.Integer(allow_none=True)
    numero_nota = ma.Decimal(allow_none=True, as_string=True)
    dt_emissao = ma.Date(allow_none=True)
    dt_vencimento = ma.Date(allow_none=True)
    valor_bruto = ma.Decimal(allow_none=True, as_string=True, places=2)
    valor_liquido = ma.Decimal(allow_none=True, as_string=True, places=2)
    descricao = ma.String(allow_none=True)
    valor_real = ma.Decimal(allow_none=True, as_string=True, places=2)
    valor_cotacao = ma.Decimal(allow_none=True, as_string=True, places=2)
    valor_final = ma.Decimal(allow_none=True, as_string=True, places=2)
    dt_pagamento = ma.Date(allow_none=True)
    status = ma.String(allow_none=True, validate=lambda x: len(x) <= 10 if x else True)
    
    # Fields from tbl_demandas
    nome_demanda = ma.String(allow_none=True)
    cliente = ma.String(allow_none=True)
    classificacao = ma.String(allow_none=True)

    @validates("id_nota")
    def validate_id_nota_non_negative(self, value, **kwargs):
        if value is not None and value < 0:
            raise ValidationError("id_nota cannot be negative.")
    
    @validates("etl_id")
    def validate_etl_id_non_negative(self, value, **kwargs):
        if value is not None and value < 0:
            raise ValidationError("etl_id cannot be negative.")

nota_fiscal_schema = NotaFiscalSchema()
nota_fiscal_list_schema = NotaFiscalSchema(many=True)
