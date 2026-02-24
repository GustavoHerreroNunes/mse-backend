from . import lifting_inspection_bp

@lifting_inspection_bp.route('/<string:lifting_type>', methods=['OPTIONS'])
@lifting_inspection_bp.route('/<int:lifting_id>/<string:lifting_type>', methods=['OPTIONS'])
def options_handler(*args, **kwargs):
    return '', 200
