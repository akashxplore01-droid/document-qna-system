import PyPDF2
import re


def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    text = ''
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() or ''
    return text


def clean_text(text):
    """Clean text by removing unwanted characters."""
    # Remove special characters and extra whitespace
    cleaned_text = re.sub(r'[^\w\s]', ' ', text)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    return cleaned_text


def chunk_text(text, chunk_size=1000):
    """Chunk text into pieces of specified size."""
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]


def extract_book_name(text):
    """Extract book name from text assuming the title is at the beginning."""
    title_match = re.match(r'^(.*?)(?:\s*\n|$)', text)
    return title_match.group(1) if title_match else 'Unknown Title'