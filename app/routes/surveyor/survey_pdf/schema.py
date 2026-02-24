from app import ma
from app.utils.base_schema import BaseSchema

class SurveyPDFSchema(BaseSchema):
    class Meta:
        primary_key = "id_survey" 
        fields = (
            "url_path_pdf",
            "url_path_pdf_signed",
            "created",
            "id_demanda",
            "verified_by_surveyor",
            "verified_by_revisor",
            "verified_by_aprovador",
        )

    url_path_pdf = ma.String(required=False)
    url_path_pdf_signed = ma.String(required=False)
    created = ma.Boolean(required=False)
    id_demanda = ma.Integer(required=True)
    verified_by_surveyor = ma.Boolean(required=False)
    verified_by_revisor = ma.Boolean(required=False)
    verified_by_aprovador = ma.Boolean(required=False)

survey_pdf_schema = SurveyPDFSchema()
survey_pdf_list_schema = SurveyPDFSchema(many=True)