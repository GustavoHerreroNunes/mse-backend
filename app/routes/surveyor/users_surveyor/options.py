from . import users_surveyor_bp

@users_surveyor_bp.route('/', methods=['OPTIONS'])
@users_surveyor_bp.route('/<int:id>', methods=['OPTIONS'])
@users_surveyor_bp.route('/email/<string:email>', methods=['OPTIONS'])
def options_handler(*args, **kwargs):
    return '', 200
