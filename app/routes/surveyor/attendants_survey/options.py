from . import attendants_survey_bp

@attendants_survey_bp.route('/', methods=['OPTIONS'])
@attendants_survey_bp.route('/task/<int:task_id>', methods=['OPTIONS'])
@attendants_survey_bp.route('/<int:attendant_id>', methods=['OPTIONS'])
def options_handler(*args, **kwargs):
    return '', 200
