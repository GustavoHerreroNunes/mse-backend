from . import customers_bp

@customers_bp.route('/', methods=['OPTIONS'])
@customers_bp.route('/<int:customer_id>', methods=['OPTIONS'])
def options_handler(*args, **kwargs):
    return '', 200
