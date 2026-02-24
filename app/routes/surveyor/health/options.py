from . import health_bp

@health_bp.route('/', methods=['OPTIONS'])
@health_bp.route('/ping', methods=['OPTIONS'])
def options_handler(*args, **kwargs):
    return '', 200
