from . import demandas_bp

@demandas_bp.route('/surveyor/<int:user_id>', methods=['OPTIONS'])
@demandas_bp.route('/<int:demanda_id>/status', methods=['OPTIONS'])
@demandas_bp.route('/<int:id_demanda>/tarefas/surveyor/', methods=['OPTIONS'])
@demandas_bp.route('/<int:demanda_id>', methods=['OPTIONS'])
@demandas_bp.route('/tarefas', methods=['OPTIONS'])
@demandas_bp.route('/', methods=['OPTIONS'])
def options_handler(*args, **kwargs):
    return '', 200