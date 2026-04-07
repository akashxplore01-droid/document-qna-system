from PyPDF2 import PdfReader
import re

def extract_text_from_pdf(pdf_path: str) -> str:
    text = ""
    try:
        pdf_reader = PdfReader(pdf_path)
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        raise Exception(f"Error extracting PDF: {str(e)}")

def clean_text(text: str) -> str:
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^
w\s.!?,;:\'\"-]', '', text)
    return text.strip()

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> list:
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunk = text[i:i + chunk_size]
        if chunk.strip():
            chunks.append(chunk)
    return chunks

def extract_book_name(text: str) -> str:
    lines = text.split('\n')[:5]
    for line in lines:
        if len(line) > 5 and len(line) < 100:
            return line.strip()
    return "Unknown Document"