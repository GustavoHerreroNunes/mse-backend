from . import auth_customer_bp

@auth_customer_bp.route('/login', methods=['OPTIONS'])
def options_handler(*args, **kwargs):
    return '', 200
