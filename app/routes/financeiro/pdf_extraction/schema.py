from marshmallow import validates, ValidationError, validate, fields
from app import ma
from app.utils.base_schema import BaseSchema

class PDFExtractionRequestSchema(BaseSchema):
    """Schema for PDF extraction request validation"""
    tipo_nota = ma.String(
        required=True,
        validate=validate.OneOf(["Invoice", "NF-e", "ND"]),
        error_messages={"invalid": "tipo_nota must be one of: Invoice, NF-e, ND"}
    )

class PDFUploadRequestSchema(BaseSchema):
    """Schema for PDF upload request validation"""
    id_demanda = ma.Integer(
        required=True,
        validate=validate.Range(min=1),
        error_messages={"invalid": "id_demanda must be a positive integer"}
    )

class NFExtractionResultSchema(BaseSchema):
    """Schema for Nota Fiscal (NF-e) extraction results"""
    numero_nota = ma.String(allow_none=True)
    data_emissao = ma.String(allow_none=True)
    data_vencimento = ma.String(allow_none=True)
    valor_bruto = ma.String(allow_none=True)
    valor_liquido = ma.String(allow_none=True)
    tipo_nota = ma.String()

class NDExtractionResultSchema(BaseSchema):
    """Schema for Nota de Débito (ND) extraction results"""
    numero_nota = ma.String(allow_none=True)
    data_emissao = ma.String(allow_none=True)
    data_vencimento = ma.String(allow_none=True)
    valor_final = ma.String(allow_none=True)
    tipo_nota = ma.String()

class InvoiceExtractionResultSchema(BaseSchema):
    """Schema for International Invoice extraction results"""
    numero_nota = ma.String(allow_none=True)
    data_emissao = ma.String(allow_none=True)
    valor_final = ma.String(allow_none=True)
    tipo_nota = ma.String()

class ExtractionResponseSchema(BaseSchema):
    """Schema for API response"""
    success = ma.Boolean()
    message = ma.String()
    extracted_data = ma.Raw(allow_none=True)

class UploadResponseSchema(BaseSchema):
    """Schema for upload API response"""
    success = ma.Boolean()
    message = ma.String()
    url = ma.String(allow_none=True)
    id_demanda = ma.Integer(allow_none=True)
    
# Schema instances
pdf_extraction_request_schema = PDFExtractionRequestSchema()
pdf_upload_request_schema = PDFUploadRequestSchema()
nf_extraction_result_schema = NFExtractionResultSchema()
nd_extraction_result_schema = NDExtractionResultSchema()
invoice_extraction_result_schema = InvoiceExtractionResultSchema()
extraction_response_schema = ExtractionResponseSchema()
upload_response_schema = UploadResponseSchema()