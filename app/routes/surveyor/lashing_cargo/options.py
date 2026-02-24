from . import lashing_cargo_bp

@lashing_cargo_bp.route('/', methods=['OPTIONS'])
@lashing_cargo_bp.route('/<int:cargo_id>', methods=['OPTIONS'])
def options_handler(*args, **kwargs):
    return '', 200
