from . import statement_of_facts_bp

@statement_of_facts_bp.route('/', methods=['OPTIONS'])
@statement_of_facts_bp.route('/cargo/', methods=['OPTIONS'])
@statement_of_facts_bp.route('/<int:event_id>', methods=['OPTIONS'])
@statement_of_facts_bp.route('/cargo/<int:event_id>', methods=['OPTIONS'])
@statement_of_facts_bp.route('/demanda/<int:demanda_id>', methods=['OPTIONS'])
@statement_of_facts_bp.route('/demanda/cargo/<int:cargo_id>', methods=['OPTIONS'])
def options_handler(*args, **kwargs):
    return '', 200
