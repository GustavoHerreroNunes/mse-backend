from . import vessel_bp

@vessel_bp.route('/', methods=['OPTIONS'])
@vessel_bp.route('/<int:vessel_id>', methods=['OPTIONS'])
@vessel_bp.route('/search', methods=['OPTIONS'])
@vessel_bp.route('/<int:vessel_id>/cranes', methods=['OPTIONS'])
@vessel_bp.route('/<int:vessel_id>/cranes/<int:crane_id>', methods=['OPTIONS'])
@vessel_bp.route('/<int:vessel_id>/cranes/<int:crane_id>/swl', methods=['OPTIONS'])
@vessel_bp.route('/<int:vessel_id>/cranes/<int:crane_id>/swl/<int:swl_capacity_id>', methods=['OPTIONS'])
def options_handler(*args, **kwargs):
    return '', 200  
