from marshmallow import validates, ValidationError
from app import ma
from app.utils.base_schema import BaseSchema
from app.utils.flexible_bool import FlexibleBoolean

class DemandaSchema(BaseSchema):
    class Meta:
        primary_key = "id_demanda"
        fields = (
            "id_demanda", "nome_demanda", "survey_status", "client_name", "client_id",
            "id_pasta_gd_demanda", "id_pasta_gd_cliente", "id_ship", "id_surveyor", "id_client",
            "executor", "numero", "conclusao", "tipo", "prioridade", "status", "horas_estimadas",
            "dt_entrega", "dt_finalizacao", "dt_abertura", "dt_requisicao", "classificacao", "descricao",
            "criador", "custo_indicativo", "custo_total", "informacoes_adicionais", "customer_name",
            "ship_name", "imo_number", "location", "have_arrived", "time_confimation", "cliente",
            "location_confirmation", "surveyor_email", "task_count", "vessel_name", "vessel_type",
            "vessel_id","opening_date", "term", "moving_to_location", "valor_acordado", "hora_extra",
            "tipo_cobranca"
        )

    id_demanda = ma.Integer(dump_only=True)
    id_surveyor = ma.Integer(required=True)
    id_ship = ma.Integer()
    id_client = ma.Integer()
    client_id = ma.Integer()
    client_name = ma.String(dump_only=True)
    id_pasta_gd_demanda = ma.String()
    id_pasta_gd_cliente = ma.String()
    cliente = ma.String()
    valor_acordado = FlexibleBoolean()
    hora_extra = ma.Boolean()
    tipo_cobranca = ma.String()

    nome_demanda = ma.String(required=True)
    executor = ma.String()
    numero = ma.String()
    conclusao = ma.String()
    tipo = ma.String()
    prioridade = ma.String()
    status = ma.String()
    horas_estimadas = ma.String()

    dt_abertura = ma.DateTime()
    opening_date = ma.Date()
    dt_requisicao = ma.DateTime()
    dt_entrega = ma.DateTime()
    term = ma.Date()
    dt_finalizacao = ma.DateTime()
    moving_to_location = FlexibleBoolean()

    classificacao = ma.String()
    descricao = ma.String()
    criador = ma.String()
    custo_indicativo = ma.Float()
    custo_total = ma.Float()
    informacoes_adicionais = ma.String()
    survey_status = ma.String()
    location = ma.String()
    have_arrived = FlexibleBoolean()
    time_confimation = ma.DateTime()
    location_confirmation = ma.String()
    surveyor_email = ma.String()

    # Campos derivados de joins
    customer_name = ma.String()
    ship_name = ma.String()
    imo_number = ma.String()
    vessel_name = ma.String()
    vessel_type = ma.String()
    vessel_id = ma.Integer()

    # Campo computado
    task_count = ma.Integer(dump_only=True)

    @validates("survey_status")
    def validate_survey_status(self, value, **kwargs):
        allowed = ["Awaiting to Start", "Pending", "Standby", "Active", "Finished"]
        if value not in allowed:
            raise ValidationError(f"Invalid survey_status. Allowed: {', '.join(allowed)}")

demanda_schema      = DemandaSchema()
demanda_list_schema = DemandaSchema(many=True)
