from . import cargo_condition_bp

@cargo_condition_bp.route('/', methods=['OPTIONS'])
@cargo_condition_bp.route('/<int:cargo_id>', methods=['OPTIONS'])
def options_handler(*args, **kwargs):
    return '', 200
