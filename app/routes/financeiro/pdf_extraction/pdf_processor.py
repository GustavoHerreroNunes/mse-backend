import re
import os
import platform
import PyPDF2
import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image
import io
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

def configure_dependencies():
    """Configure Tesseract and Poppler based on environment"""
    system = platform.system().lower()
    
    if system == "windows":
        # Configure Tesseract for Windows
        possible_tesseract_paths = [
            r'C:\Program Files\Tesseract-OCR\tesseract.exe',
            r'C:\Users\{}\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'.format(os.getenv('USERNAME', '')),
        ]
        
        for path in possible_tesseract_paths:
            if os.path.exists(path):
                pytesseract.pytesseract.tesseract_cmd = path
                logger.info(f"Tesseract configured at: {path}")
                break
        else:
            pytesseract.pytesseract.tesseract_cmd = 'tesseract'
            logger.warning("Tesseract not found in common paths, assuming it's in PATH")
        
        # Configure Poppler for Windows
        possible_poppler_paths = [
            r'C:\Program Files\poppler-25.07.0\Library\bin',
            r'C:\poppler-windows\Library\bin',
            r'C:\Program Files\poppler\bin',
            r'C:\poppler\bin',
        ]
        
        poppler_path = None
        for path in possible_poppler_paths:
            if os.path.exists(path):
                poppler_path = path
                logger.info(f"Poppler found at: {path}")
                break
        
        if not poppler_path:
            logger.warning("Poppler not found in common paths, assuming it's in PATH")
            
        return poppler_path
        
    else:
        # Linux/Cloud environment (GCP Cloud Run)
        pytesseract.pytesseract.tesseract_cmd = 'tesseract'
        
        # Set language data path for cloud environment
        if 'TESSDATA_PREFIX' not in os.environ:
            os.environ['TESSDATA_PREFIX'] = '/usr/share/tesseract-ocr/5/tessdata/'
        
        logger.info("Configured for Linux/Cloud environment")
        return None  # Poppler should be in PATH in Linux

# Configure dependencies on module import
POPPLER_PATH = configure_dependencies()

# Development flag for testing without full OCR setup
DEVELOPMENT_MODE = os.getenv('PDF_EXTRACTION_DEV_MODE', 'false').lower() == 'true'

class PDFProcessor:
    """
    Class responsible for processing PDF files and extracting text content.
    Handles both selectable text PDFs and image-based PDFs using OCR.
    """
    
    def __init__(self):
        # Dependencies are configured at module level
        pass
    
    def extract_text_from_pdf(self, pdf_content: bytes) -> str:
        """
        Extract text from PDF content.
        First tries to extract selectable text, if that fails, uses OCR.
        
        Args:
            pdf_content: PDF file content as bytes
            
        Returns:
            Extracted text as string
            
        Raises:
            Exception: If text extraction fails
        """
        try:
            # First, try to extract selectable text
            text = self._extract_selectable_text(pdf_content)
            
            # If no meaningful text found, use OCR
            if not text or len(text.strip()) < 50:
                logger.info("PDF appears to be image-based, attempting OCR extraction")
                text = self._extract_text_with_ocr(pdf_content)
            
            return text
            
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {str(e)}")
            raise Exception(f"Failed to extract text from PDF: {str(e)}")
    
    def _extract_selectable_text(self, pdf_content: bytes) -> str:
        """Extract selectable text from PDF using PyPDF2"""
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
            text = ""
            
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return text
            
        except Exception as e:
            logger.warning(f"Failed to extract selectable text: {str(e)}")
            return ""
    
    def _extract_text_with_ocr(self, pdf_content: bytes) -> str:
        """Extract text from PDF using OCR (Tesseract) with improved error handling"""
        try:
            logger.info("Starting OCR extraction...")
            
            # Convert PDF to images with Poppler path configuration
            if POPPLER_PATH:
                # Windows with specific Poppler path
                images = convert_from_bytes(pdf_content, poppler_path=POPPLER_PATH)
            else:
                # Linux and Poppler in PATH
                images = convert_from_bytes(pdf_content)
            
            logger.info(f"Converted PDF to {len(images)} images")
            
            text = ""
            for i, image in enumerate(images):
                logger.info(f"Processing page {i+1}/{len(images)}")
                # Use OCR to extract text from each page
                page_text = pytesseract.image_to_string(image, lang='por+eng')
                text += page_text + "\n"
            
            logger.info("OCR extraction completed successfully")
            return text
            
        except Exception as e:
            error_msg = str(e).lower()
            logger.warning(error_msg)
            if "poppler" in error_msg or "unable to get page count" in error_msg:
                logger.error("Poppler not found or not properly configured")
                raise Exception(
                    "Poppler is required for OCR processing. "
                    "Please install Poppler: https://github.com/oschwartz10612/poppler-windows/releases/ "
                    f"Original error: {str(e)}"
                )
            elif "tesseract" in error_msg:
                logger.error("Tesseract not found or not properly configured")
                raise Exception(
                    "Tesseract OCR is required for image-based PDF processing. "
                    f"Original error: {str(e)}"
                )
            else:
                logger.error(f"OCR extraction failed: {str(e)}")
                raise Exception(f"OCR extraction failed: {str(e)}")

    def validate_pdf_content(self, pdf_content: bytes) -> bool:
        """
        Validate if the content is a valid PDF with extractable text.
        
        Args:
            pdf_content: PDF file content as bytes
            
        Returns:
            True if valid PDF with text, False otherwise
        """
        try:
            # Check if it's a valid PDF
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
            
            # Check if we can extract any text
            text = self.extract_text_from_pdf(pdf_content)
            
            # Must have at least some meaningful content
            return len(text.strip()) > 10
            
        except Exception as e:
            logger.error(f"PDF validation failed: {str(e)}")
            return False


class InvoiceDataExtractor:
    """
    Class responsible for extracting specific data from different types of invoices.
    """
    
    def __init__(self):
        self.pdf_processor = PDFProcessor()
    
    def extract_data(self, pdf_content: bytes, tipo_nota: str) -> Dict[str, Any]:
        """
        Main method to extract data from PDF based on invoice type.
        
        Args:
            pdf_content: PDF file content as bytes
            tipo_nota: Type of invoice ("NF-e", "ND", "Invoice")
            
        Returns:
            Dictionary with extracted data
        """
        # Extract text from PDF
        text = self.pdf_processor.extract_text_from_pdf(pdf_content)
        
        # Extract data based on invoice type
        if tipo_nota == "NF-e":
            return self._extract_nf_data(text)
        elif tipo_nota == "ND":
            return self._extract_nd_data(text)
        elif tipo_nota == "Invoice":
            return self._extract_invoice_data(text)
        else:
            raise ValueError(f"Invalid invoice type: {tipo_nota}")
    
    def _extract_nf_data(self, text: str) -> Dict[str, Any]:
        """Extract data from Nota Fiscal Eletrônica (NF-e)"""
        data = {
            "tipo_nota": "NF-e",
            "numero_nota": None,
            "data_emissao": None,
            "data_vencimento": None,
            "valor_bruto": None,
            "valor_liquido": None
        }
        
        try:
            # Número da Nota (pattern: any length number after newline)
            numero_match = re.search(r'Número da NFS-e\s*\n\s*(\d+)', text, re.IGNORECASE)
            if numero_match:
                data["numero_nota"] = numero_match.group(1)
            
            # Data de emissão (pattern: dd/mm/yyyy after newline)
            emissao_match = re.search(r'Data e Hora da emissão da NFS-e\s*\n\s*(\d{2}/\d{2}/\d{4})', text, re.IGNORECASE)
            if emissao_match:
                data["data_emissao"] = emissao_match.group(1)
            
            # Data de vencimento (pattern: Vencimento: dd/mm/yyyy)
            vencimento_match = re.search(r'Vencimento:\s*(\d{2}/\d{2}/\d{4})', text, re.IGNORECASE)
            if vencimento_match:
                data["data_vencimento"] = vencimento_match.group(1)
            
            # Valor bruto (pattern: Valor do Serviço followed by newline and R$)
            valor_bruto_match = re.search(r'Valor do Serviço\s*\n\s*R\$\s*([\d.,]+)', text, re.IGNORECASE)
            if valor_bruto_match:
                data["valor_bruto"] = valor_bruto_match.group(1)
            
            # Valor líquido (pattern: Valor Líquido da NFS-e followed by newline and R$)
            valor_liquido_match = re.search(r'Valor Líquido da NFS-e\s*\n\s*R\$\s*([\d.,]+)', text, re.IGNORECASE)
            if valor_liquido_match:
                data["valor_liquido"] = valor_liquido_match.group(1)
            
        except Exception as e:
            logger.error(f"Error extracting NF-e data: {str(e)}")
        
        return data
    
    def _extract_nd_data(self, text: str) -> Dict[str, Any]:
        """Extract data from Nota de Débito (ND)"""
        data = {
            "tipo_nota": "ND",
            "numero_nota": None,
            "data_emissao": None,
            "data_vencimento": None,
            "valor_final": None
        }
        
        try:
            # Número da nota
            numero_match = re.search(r'NOTA DE DÉBITO\s+nº\s+(\d+)', text, re.IGNORECASE)
            if numero_match:
                data["numero_nota"] = numero_match.group(1)
            
            # Data de emissão (Portuguese month names)
            meses_pt = {
                'janeiro': '01', 'fevereiro': '02', 'março': '03', 'abril': '04',
                'maio': '05', 'junho': '06', 'julho': '07', 'agosto': '08',
                'setembro': '09', 'outubro': '10', 'novembro': '11', 'dezembro': '12'
            }
            
            emissao_match = re.search(r'Emissão:\s*[^,]+,\s*(\d{1,2})\s+de\s+(\w+)\s+de\s+(\d{4})', text, re.IGNORECASE)
            if emissao_match:
                dia = emissao_match.group(1).zfill(2)
                mes_nome = emissao_match.group(2).lower()
                ano = emissao_match.group(3)
                
                if mes_nome in meses_pt:
                    mes = meses_pt[mes_nome]
                    data["data_emissao"] = f"{dia}/{mes}/{ano}"
            
            # Data de vencimento e valor final (same pattern)
            vencimento_match = re.search(r'Vencimento:\s+dia\s+(\d{2}/\d{2}/\d{4})\s+no\s+valor\s+de\s+R\$\s*([\d.,]+)', text, re.IGNORECASE)
            if vencimento_match:
                data["data_vencimento"] = vencimento_match.group(1)
                data["valor_final"] = vencimento_match.group(2)
            
        except Exception as e:
            logger.error(f"Error extracting ND data: {str(e)}")
        
        return data
    
    def _extract_invoice_data(self, text: str) -> Dict[str, Any]:
        """Extract data from International Invoice"""
        data = {
            "tipo_nota": "Invoice",
            "numero_nota": None,
            "data_emissao": None,
            "valor_final": None
        }
        
        try:
            # Número da nota (pattern: valor/ano)
            numero_match = re.search(r'Invoice\s+No\.:\s*(\d+/\d+)', text, re.IGNORECASE)
            if numero_match:
                data["numero_nota"] = numero_match.group(1)
            
            # Data de emissão (English month names)
            meses_en = {
                'january': '01', 'february': '02', 'march': '03', 'april': '04',
                'may': '05', 'june': '06', 'july': '07', 'august': '08',
                'september': '09', 'october': '10', 'november': '11', 'december': '12'
            }
            
            emissao_match = re.search(r'Brazil,\s+([\w\s]{3,12}?)\s+(\d{1,2})(?:st|nd|rd|th)?,\s+(\d{4})', text, re.IGNORECASE)
            if emissao_match:
                logger.info("Emissao match for invoice")
                mes_raw = emissao_match.group(1).lower()
                dia = emissao_match.group(2).zfill(2)
                ano = emissao_match.group(3)
                
                mes_clean = re.sub(r'\s+', '', mes_raw).lower()

                if mes_clean in meses_en:
                    mes = meses_en[mes_clean]
                    data["data_emissao"] = f"{dia}/{mes}/{ano}"
            
            # Valor final
            valor_match = re.search(r'Total\s+Value:\s+USD\s+([\d.,]+)', text, re.IGNORECASE)
            if valor_match:
                data["valor_final"] = valor_match.group(1)
            
        except Exception as e:
            logger.error(f"Error extracting Invoice data: {str(e)}")
        
        return data