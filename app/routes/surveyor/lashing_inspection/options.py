from . import lashing_inspection_bp

@lashing_inspection_bp.route('/<string:lashing_type>', methods=['OPTIONS'])
@lashing_inspection_bp.route('/<int:lashing_id>/<string:lashing_type>', methods=['OPTIONS'])
def options_handler(*args, **kwargs):
    return '', 200
