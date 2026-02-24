from . import lifting_material_bp

@lifting_material_bp.route('/', methods=['OPTIONS'])
@lifting_material_bp.route('/all/<int:id_task>', methods=['OPTIONS'])
@lifting_material_bp.route('/<int:id_lifting_material>', methods=['OPTIONS'])
def options_handler(*args, **kwargs):
    return '', 200
