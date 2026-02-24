from . import notifications_customer_bp

@notifications_customer_bp.route('/', methods=['OPTIONS'])
@notifications_customer_bp.route('/<int:notification_id>', methods=['OPTIONS'])
@notifications_customer_bp.route('/user/<int:user_id>', methods=['OPTIONS'])
def options_handler(*args, **kwargs):
    return '', 200