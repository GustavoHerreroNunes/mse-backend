from . import medicoes_bp

@medicoes_bp.route('/', methods=['OPTIONS'])
@medicoes_bp.route('/demanda/<int:demanda_id>', methods=['OPTIONS'])
@medicoes_bp.route('/medicao/<int:medicao_id>', methods=['OPTIONS'])
@medicoes_bp.route('/export_csv', methods=['OPTIONS'])
def options_handler(*args, **kwargs):
    return '', 200
