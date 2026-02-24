from . import lashing_material_bp

@lashing_material_bp.route('/', methods=['OPTIONS'])
@lashing_material_bp.route('/all/<int:id_task>', methods=['OPTIONS'])
@lashing_material_bp.route('/<int:id_lashing_material>', methods=['OPTIONS'])
def options_handler(*args, **kwargs):
    return '', 200
