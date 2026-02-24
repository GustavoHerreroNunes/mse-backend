from . import auth_surveyor_bp

@auth_surveyor_bp.route('/login', methods=['OPTIONS'])
def options_handler(*args, **kwargs):
    return '', 200
