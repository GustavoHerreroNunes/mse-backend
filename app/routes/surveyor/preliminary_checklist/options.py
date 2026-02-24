from . import checklist_bp

@checklist_bp.route('/', methods=['OPTIONS'])
@checklist_bp.route('/<int:id_survey>', methods=['OPTIONS'])
def options_handler(*args, **kwargs):
    return '', 200
