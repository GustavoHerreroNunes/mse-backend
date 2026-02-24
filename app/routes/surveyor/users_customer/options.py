from . import users_customer_bp

@users_customer_bp.route('/', methods=['OPTIONS'])
@users_customer_bp.route('/<int:id>', methods=['OPTIONS'])
@users_customer_bp.route('/email/<string:email>', methods=['OPTIONS'])
def options_handler(*args, **kwargs):
    return '', 200
