"""PDF Processing Module"""
import pdfplumber
from PyPDF2 import PdfReader


class PDFProcessor:
    def __init__(self, chunk_size=300, chunk_overlap=50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def extract_text(self, pdf_path):
        """Extract text from PDF"""
        text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n\n"
        except:
            reader = PdfReader(pdf_path)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"
        return text.strip()
    
    def chunk_text(self, text):
        """Split text into chunks"""
        chunks = []
        paragraphs = text.split('\n\n')
        current = ""
        idx = 0
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            if len(current) + len(para) > self.chunk_size and current:
                chunks.append({"id": idx, "text": current.strip(), "char_count": len(current.strip())})
                idx += 1
                words = current.split()[-self.chunk_overlap:]
                current = " ".join(words) + " " + para
            else:
                current = current + " " + para if current else para
        
        if current.strip():
            chunks.append({"id": idx, "text": current.strip(), "char_count": len(current.strip())})
        return chunks
    
    def process_pdf(self, pdf_path):
        """Process PDF and return chunks"""
        text = self.extract_text(pdf_path)
        if not text:
            raise ValueError("No text extracted from PDF")
        return self.chunk_text(text)
