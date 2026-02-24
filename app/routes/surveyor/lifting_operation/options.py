from . import lifting_operation_bp

@lifting_operation_bp.route('/', methods=['OPTIONS'])
@lifting_operation_bp.route('/<int:cargo_id>', methods=['OPTIONS'])
def options_handler(*args, **kwargs):
    return '', 200
