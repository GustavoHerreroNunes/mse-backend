from . import notifications_bp

@notifications_bp.route('/', methods=['OPTIONS'])
@notifications_bp.route('/<int:notification_id>', methods=['OPTIONS'])
@notifications_bp.route('/user/<int:user_id>', methods=['OPTIONS'])
@notifications_bp.route('/user/<int:user_id>/unread-count', methods=['OPTIONS'])
@notifications_bp.route('/<int:notification_id>/toggle-read', methods=['OPTIONS'])
def options_handler(*args, **kwargs):
    return '', 200