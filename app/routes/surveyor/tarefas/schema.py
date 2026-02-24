from app import ma
from app.utils.base_schema import BaseSchema

class TarefasSchema(BaseSchema):
    class Meta:
        primary_key = "id_tarefas"
        fields = (
            "numero", "descricao", "nome_tarefa", "dt_requisicao", "dt_abertura",
            "horas_estimadas", "atividade", "cod_atividade", "cliente", "prioridade",
            "status", "tipo", "demanda", "dt_finalizacao", "dt_prazo", "nome_demanda",
            "executor", "comentario_exec", "revisor", "comentario_revisor", "classificacao",
            "comentado_por", "dt_comentario_extra", "comentario_extra", "dt_comentario_exec_rev",
            "comentado_por_extra", "dt_coment_validacao", "coment_por_validacao", "coment_validacao",
            "created_time", "hh_total", "aprovada_por", "id_pasta_tarefa", "custo_indicativo",
            "custo_total", "document_type", "service_type", "sequential_number", "document_review",
            "id_tarefas"
        )

    numero = ma.String()
    descricao = ma.String()
    nome_tarefa = ma.String()
    dt_requisicao = ma.DateTime()
    dt_abertura = ma.DateTime()
    horas_estimadas = ma.Integer()
    atividade = ma.String()
    cod_atividade = ma.String()
    cliente = ma.String()
    prioridade = ma.String()
    status = ma.String()
    tipo = ma.String()
    demanda = ma.Integer()
    dt_finalizacao = ma.DateTime()
    dt_prazo = ma.DateTime()
    nome_demanda = ma.String()
    executor = ma.String()
    comentario_exec = ma.String()
    revisor = ma.String()
    comentario_revisor = ma.String()
    classificacao = ma.String()
    comentado_por = ma.String()
    dt_comentario_extra = ma.DateTime()
    comentario_extra = ma.String()
    dt_comentario_exec_rev = ma.DateTime()
    comentado_por_extra = ma.String()
    dt_coment_validacao = ma.DateTime()
    coment_por_validacao = ma.String()
    coment_validacao = ma.String()
    created_time = ma.DateTime()
    hh_total = ma.String()
    aprovada_por = ma.String()
    id_pasta_tarefa = ma.String()
    custo_indicativo = ma.Integer()
    custo_total = ma.Integer()
    document_type = ma.String()
    service_type = ma.String()
    sequential_number = ma.String()
    document_review = ma.String()
    id_tarefas = ma.Integer()

tarefas_schema = TarefasSchema()
tarefas_list_schema = TarefasSchema(many=True)