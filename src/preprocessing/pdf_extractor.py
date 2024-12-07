import pdfplumber
import logging
from typing import Optional, List
from pathlib import Path

logger = logging.getLogger(__name__)

class PDFExtractor:
    """Handles the extraction of text from PDF documents."""
    
    def __init__(self):
        self.supported_languages = ['en']  # Add more languages as needed
        self._pages = []  # Store pages for later use
        
    def extract_text(self, pdf_path: str) -> str:
        """
        Extract text content from a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text as a string
        """
        if not Path(pdf_path).exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
            
        try:
            extracted_text = []
            with pdfplumber.open(pdf_path) as pdf:
                self._pages = pdf.pages  # Store pages
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        extracted_text.append(text)
            
            return '\n'.join(extracted_text)
            
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {str(e)}")
            raise

    def get_page_count(self) -> List[str]:
        """
        Get the list of pages from the last processed PDF.
        
        Returns:
            List of pages
        """
        return self._pages