from marshmallow import validates, ValidationError
from app import ma
from app.utils.base_schema import BaseSchema
from app.utils.flexible_bool import FlexibleBoolean

class TasksSurveySchema(BaseSchema):
    class Meta:
        primary_key = "id_task"
        fields = (
            "id_task", "id_survey", "id_user", "task_title", "task_description", 
            "finished", "last_task_done", "num_bollards_fwd", "num_bollards_aft", 
            "finished_mark_one", "finished_mark_two", "finished_mark_three",
            "vessel_condition", "external_cranes", "wire", "sheaves", "operation_condition",
            "storage_adequate"
        )
    
    id_task = ma.Integer(dump_only=True)
    id_survey = ma.Integer(required=True)
    id_user = ma.Integer(required=True)
    task_title = ma.String(required=True)
    task_description = ma.String(required=True)
    finished = FlexibleBoolean(required=False)
    last_task_done = ma.Integer(required=False)
    num_bollards_fwd = ma.Integer(required=False)
    num_bollards_aft = ma.Integer(required=False)
    finished_mark_one = FlexibleBoolean(required=False)
    finished_mark_two = FlexibleBoolean(required=False)
    finished_mark_three = FlexibleBoolean(required=False)
    vessel_condition = ma.String(required=False)
    external_cranes = ma.String(required=False)
    wire = ma.String(required=False)
    sheaves = ma.String(required=False)
    operation_condition = ma.String(required=False)
    storage_adequate = ma.String(required=False)

    @validates("id_survey", "id_user", "num_bollards_fwd", "num_bollards_aft")
    def validate_non_negative_values(self, value, **kwargs):
        if value is not None and value < 0:
            raise ValidationError('Value cannot be negative.')

class CommentSchema(BaseSchema):
    class Meta:
        primary_key = "id_comment"
        fields = ("id_comment", "id_task", "section_index", "sub_section_index", "message", 
                  "id_cargo", "id_lifting_material", "id_lashing_material")
    
    id_comment = ma.Integer(dump_only=True)
    id_task = ma.Integer(required=True)
    sub_section_index = ma.Integer(required=True)
    section_index = ma.Integer(required=True)
    message = ma.String(required=True)
    id_cargo = ma.Integer(allow_none=True)
    id_lifting_material = ma.Integer(allow_none=True)
    id_lashing_material = ma.Integer(allow_none=True)
    
    @validates("section_index")
    def validate_section_index(self, value, **kwargs):
        if value < 0:
            raise ValidationError('Section index cannot be negative.')

class PhotoSchema(ma.Schema):
    class Meta:
        fields = ("id_photo", "id_task", "section_index", "sub_section_index", 
                  "id_cargo", "url_path", "id_lifting_material", "id_lashing_material",
                  "url_path_cliente")
    
    id_photo = ma.Integer(dump_only=True)
    id_task = ma.Integer(required=True)
    section_index = ma.Integer(required=True)
    sub_section_index = ma.Integer(required=False)
    id_cargo = ma.Integer(required=False)
    id_lifting_material = ma.Integer(required=False)
    id_lashing_material = ma.Integer(required=False)
    url_path = ma.String(required=True)
    url_path_cliente = ma.String(required=False)
    
    @validates("section_index", "sub_section_index")
    def validate_section_index(self, value, **kwargs):
        if value < 0:
            raise ValidationError('Section and sub section indexes cannot be negative.')

task_survey_schema = TasksSurveySchema()
task_survey_list_schema = TasksSurveySchema(many=True)

comment_schema = CommentSchema()
comment_list_schema = CommentSchema(many=True)

photo_schema = PhotoSchema()
photo_list_schema = PhotoSchema(many=True)
