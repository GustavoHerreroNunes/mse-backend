from . import cargo_inspection_bp

@cargo_inspection_bp.route('/<string:cargo_type>', methods=['OPTIONS'])
@cargo_inspection_bp.route('/<int:cargo_id>/<string:cargo_type>', methods=['OPTIONS'])
def options_handler(*args, **kwargs):
    return '', 200
