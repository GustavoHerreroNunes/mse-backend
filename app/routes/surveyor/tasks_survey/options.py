from . import tasks_survey_bp

# Add options handler for CORS preflight requests
@tasks_survey_bp.route('/boarding', methods=['OPTIONS'])
@tasks_survey_bp.route('/boarding/<int:task_id>', methods=['OPTIONS'])
@tasks_survey_bp.route('/boarding/comments', methods=['OPTIONS'])
@tasks_survey_bp.route('/boarding/comments/<int:comment_id>', methods=['OPTIONS'])
@tasks_survey_bp.route('/boarding/comments/task/<int:task_id>', methods=['OPTIONS'])
@tasks_survey_bp.route('/boarding/photos', methods=['OPTIONS'])
@tasks_survey_bp.route('/boarding/photos/<int:photo_id>', methods=['OPTIONS'])
@tasks_survey_bp.route('/boarding/photos/task/<int:task_id>', methods=['OPTIONS'])
@tasks_survey_bp.route('/boarding/photos/task/<int:task_id>/section/<int:section_index>', methods=['OPTIONS'])
@tasks_survey_bp.route('/boarding/photos/task/<int:task_id>/section/<int:section_index>/subsection/<int:subsection_index>', methods=['OPTIONS'])
@tasks_survey_bp.route('/boarding/comments/cargo/<int:id_cargo>/subsection/<int:sub_section_index>', methods=['OPTIONS'])
@tasks_survey_bp.route('/boarding/comments/lashing/<int:id_lashing>/subsection/<int:sub_section_index>', methods=['OPTIONS'])
@tasks_survey_bp.route('/boarding/comments/lifting/<int:id_lifting>/subsection/<int:sub_section_index>', methods=['OPTIONS'])
@tasks_survey_bp.route('/boarding/comments/task/<int:task_id>/section/<int:section_index>', methods=['OPTIONS'])
@tasks_survey_bp.route('/boarding/comments/task/<int:task_id>/section/<int:section_index>/subsection/<int:subsection_index>', methods=['OPTIONS'])
def options_handler(*args, **kwargs):
    return '', 200
