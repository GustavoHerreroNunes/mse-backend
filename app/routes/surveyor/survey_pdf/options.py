from . import survey_pdf_bp

@survey_pdf_bp.route('/', methods=['OPTIONS'])
@survey_pdf_bp.route('/<int:id_demanda>', methods=['OPTIONS'])
@survey_pdf_bp.route('/survey/pdf', methods=['OPTIONS'])
def options_handler(*args, **kwargs):
    return '', 200
