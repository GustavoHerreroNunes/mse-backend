# PDF Invoice Data Extraction API

## Overview

This module provides PDF data extraction functionality for different types of Brazilian and international invoices. It can process both selectable text PDFs and image-based PDFs using OCR technology.

## Supported Invoice Types

### 1. NF-e (Nota Fiscal Eletrônica)
Brazilian electronic invoice for national transactions.

**Extracted Data:**
- `numero_nota`: Invoice number (8-digit pattern)
- `data_emissao`: Issue date (dd/mm/yyyy format)
- `data_vencimento`: Due date (dd/mm/yyyy format)
- `valor_bruto`: Gross amount
- `valor_liquido`: Net amount

**Text Patterns:**
- Number: "Número da Nota" followed by 8 digits
- Issue date: "Data e Hora de Emissão" followed by date
- Due date: "Vencimento = dd/mm/yyyy"
- Gross value: "VALOR DA NOTA = R$<valor>"
- Net value: "Valor Liquido R$<valor>"

### 2. ND (Nota de Débito)
Brazilian debit note invoice.

**Extracted Data:**
- `numero_nota`: Invoice number
- `data_emissao`: Issue date (dd/mm/yyyy format)
- `data_vencimento`: Due date (dd/mm/yyyy format)
- `valor_final`: Final amount

**Text Patterns:**
- Number: "NOTA DE DÉBITO nº 0000000000"
- Issue date: "Emissão: <local>, dd de Month de yyyy" (Portuguese months)
- Due date & amount: "Vencimento: dia dd/mm/yyyy no valor de R$<valor>"

### 3. Invoice (International)
International invoices for foreign customers.

**Extracted Data:**
- `numero_nota`: Invoice number (valor/ano format)
- `data_emissao`: Issue date (dd/mm/yyyy format)
- `valor_final`: Final amount in USD

**Text Patterns:**
- Number: "Invoice No.: <valor>/<ano>"
- Issue date: "Brazil, Month ddth, yyyy" (English months)
- Final amount: "Total Value: USD <valor>"

## API Endpoints

### POST /pdf_extraction/extract

Extracts data from PDF invoice files.

**Request Format:** `multipart/form-data`

**Parameters:**
- `file`: PDF file (required)
- `data`: JSON string with `tipo_nota` field (required)

**Example Request:**
```bash
curl -X POST \
  http://localhost:5000/pdf_extraction/extract \
  -H "Content-Type: multipart/form-data" \
  -F "file=@invoice.pdf" \
  -F 'data={"tipo_nota": "NF-e"}'
```

**Valid `tipo_nota` values:**
- `"NF-e"` - Nota Fiscal Eletrônica
- `"ND"` - Nota de Débito
- `"Invoice"` - International Invoice

### POST /pdf_extraction/upload

Uploads PDF invoice files to Google Drive.

**Request Format:** `multipart/form-data`

**Parameters:**
- `file`: PDF file (required)
- `data`: JSON string with `id_demanda` field (required)

**Example Request:**
```bash
curl -X POST \
  http://localhost:5000/pdf_extraction/upload \
  -H "Content-Type: multipart/form-data" \
  -F "file=@invoice.pdf" \
  -F 'data={"id_demanda": 123}'
```

**Required fields:**
- `id_demanda`: Integer ID of the demanda to associate with the invoice

## Response Format

### Success Response (200) - Extract Endpoint
```json
{
  "success": true,
  "message": "Data extracted successfully",
  "extracted_data": {
    "tipo_nota": "NF-e",
    "numero_nota": "12345678",
    "data_emissao": "15/10/2024",
    "data_vencimento": "15/11/2024",
    "valor_bruto": "1.500,00",
    "valor_liquido": "1.275,00"
  }
}
```

### Success Response (200) - Upload Endpoint
```json
{
  "success": true,
  "message": "Invoice PDF uploaded successfully to Google Drive",
  "url": "https://drive.google.com/uc?id=FILE_ID&export=download",
  "id_demanda": 123
}
```

### Error Response (4xx/5xx)
```json
{
  "success": false,
  "message": "Error description",
  "extracted_data": null
}
```

## Error Codes

- **400 Bad Request:** 
  - No file in request
  - Invalid file type (not PDF)
  - Invalid JSON format
  - Invalid `tipo_nota` value (extract endpoint)
  - Missing `id_demanda` field (upload endpoint)
  - PDF without extractable text (extract endpoint)

- **404 Not Found:**
  - Demanda not found (upload endpoint)

- **500 Internal Server Error:**
  - PDF processing error
  - OCR extraction failure
  - Google Drive upload failure
  - Unexpected server error

## Features

### 1. PDF Text Extraction
- **Selectable Text**: Uses PyPDF2 for direct text extraction
- **OCR Processing**: Falls back to Tesseract OCR for image-based PDFs
- **Automatic Detection**: Determines if OCR is needed based on text content

### 2. File Validation
- Validates PDF file format
- Ensures PDF contains extractable text
- Checks for minimum text content

### 3. Data Pattern Matching
- Uses regex patterns specific to each invoice type
- Handles Portuguese and English date formats
- Extracts monetary values with proper formatting

## Dependencies

Add these to your `requirements.txt`:
```
PyPDF2==3.0.1
pytesseract==0.3.10
pdf2image==1.16.3
Pillow==10.0.1
```

## OCR Setup

### Windows
1. Download Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install with Portuguese and English language packs
3. Add Tesseract to your PATH or update the path in `pdf_processor.py`:
   ```python
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   ```

### Linux/macOS
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install tesseract-ocr tesseract-ocr-por tesseract-ocr-eng

# macOS
brew install tesseract tesseract-lang
```

## Testing

Use the provided test script to validate the API:

```bash
python test_pdf_extraction.py
```

## Module Structure

```
app/routes/financeiro/pdf_extraction/
├── __init__.py              # Blueprint configuration
├── extract_invoice_data.py  # Main API endpoint
├── pdf_processor.py         # PDF processing and OCR logic
├── schema.py               # Marshmallow schemas for validation
└── options.py              # CORS OPTIONS handler
```

## Usage Examples

### Python Requests
```python
import requests
import json

files = {'file': ('invoice.pdf', open('invoice.pdf', 'rb'), 'application/pdf')}
data = {'data': json.dumps({"tipo_nota": "NF-e"})}

response = requests.post(
    'http://localhost:5000/pdf_extraction/extract',
    files=files,
    data=data
)

print(response.json())
```

### JavaScript/Fetch
```javascript
const formData = new FormData();
formData.append('file', pdfFile);
formData.append('data', JSON.stringify({"tipo_nota": "NF-e"}));

fetch('/pdf_extraction/extract', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

## Performance Considerations

1. **OCR Processing**: Image-based PDFs take significantly longer to process
2. **File Size**: Large PDF files may require increased timeout settings
3. **Memory Usage**: OCR processing can be memory-intensive for large files
4. **Language Packs**: Ensure proper language packs are installed for better OCR accuracy

## Troubleshooting

### Common Issues

1. **"Tesseract not found"**
   - Install Tesseract OCR
   - Set correct path in `pdf_processor.py`

2. **"PDF without extractable text"**
   - PDF might be corrupted
   - Try with a different PDF file
   - Check if OCR dependencies are properly installed

3. **Poor extraction accuracy**
   - Ensure PDF quality is good
   - Check if correct language packs are installed
   - Verify regex patterns match your document format

### Debug Mode

Enable debug logging to troubleshoot issues:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Security Considerations

1. **File Validation**: Only PDF files are accepted
2. **File Size Limits**: Consider implementing file size limits
3. **Input Sanitization**: All inputs are validated using Marshmallow schemas
4. **Error Handling**: Sensitive error details are not exposed to clients