from . import relation_bp

@relation_bp.route('/', methods=['OPTIONS'])
@relation_bp.route('/<string:relation_type>/<int:id_rlt>', methods=['OPTIONS'])
def options_handler(*args, **kwargs):
    return '', 200
