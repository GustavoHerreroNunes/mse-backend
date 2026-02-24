from . import cargo_storage_bp

@cargo_storage_bp.route('/', methods=['OPTIONS'])
@cargo_storage_bp.route('/<int:cargo_id>', methods=['OPTIONS'])
def options_handler(*args, **kwargs):
    return '', 200
