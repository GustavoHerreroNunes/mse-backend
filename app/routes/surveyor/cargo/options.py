from . import cargo_bp

@cargo_bp.route('/', methods=['OPTIONS'])
@cargo_bp.route('/<int:cargo_id>', methods=['OPTIONS'])
def options_handler(*args, **kwargs):
    return '', 200
