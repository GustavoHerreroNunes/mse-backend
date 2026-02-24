from . import tarefas_bp

@tarefas_bp.route('/', methods=['OPTIONS'])
@tarefas_bp.route('/<int:id_demanda>', methods=['OPTIONS'])
def options_handler(*args, **kwargs):
    return '', 200
