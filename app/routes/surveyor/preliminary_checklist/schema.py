from app import ma
from app.utils.base_schema import BaseSchema
from app.utils.flexible_bool import FlexibleBoolean

class ChecklistSchema(BaseSchema):
    class Meta:
        primary_key = "id_survey" 
        fields = (
            "received_packing", "loi", "received_lifting", "received_stowage",
            "received_seafastening", "contact_terminal", "contact_port",
            "contact_vessel", "is_finished", "id_survey"
        )

    id_survey = ma.Integer(required=True)
    received_packing = ma.String(required=False)
    loi = ma.String(required=False)
    received_lifting = ma.String(required=False)
    received_stowage = ma.String(required=False)
    received_seafastening = ma.String(required=False)
    contact_terminal = ma.String(required=False)
    contact_port = ma.String(required=False)
    contact_vessel = ma.String(required=False)
    is_finished = FlexibleBoolean(required=False)

checklist_schema = ChecklistSchema()
checklist_list_schema = ChecklistSchema(many=True)