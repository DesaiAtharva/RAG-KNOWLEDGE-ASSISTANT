import io
from typing import List
from PyPDF2 import PdfReader

class DocumentProcessor:
    def __init__(self, chunk_size: int = 300, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def extract_text_from_pdf(self, file_content: bytes) -> str:
        pdf_file = io.BytesIO(file_content)
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text

    def split_text(self, text: str) -> List[str]:
        # Simple recursive splitting logic
        if len(text) <= self.chunk_size:
            return [text]
        
        chunks = []
        start = 0
        while start < len(text):
            end = start + self.chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start += self.chunk_size - self.chunk_overlap
        return chunks

    def process_file(self, file_content: bytes, filename: str) -> List[str]:
        if filename.endswith(".pdf"):
            text = self.extract_text_from_pdf(file_content)
        else:
            text = file_content.decode("utf-8")
        
        return self.split_text(text)
