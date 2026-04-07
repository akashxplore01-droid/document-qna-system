from fastapi import APIRouter, UploadFile, File, HTTPException
from app.utils.pdf_processor import extract_text_from_pdf, chunk_text, extract_book_name, clean_text
from app.services.embeddings import embedding_service
from app.services.vector_db import vector_db
import os

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        
        text = extract_text_from_pdf(file_path)
        cleaned_text = clean_text(text)
        chunks = chunk_text(cleaned_text)
        
        embeddings = embedding_service.get_embeddings_batch(chunks)
        vector_db.add_documents(embeddings, chunks)
        
        book_name = extract_book_name(text)
        
        return {
            "filename": file.filename,
            "book_name": book_name,
            "chunks": len(chunks),
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/list")
async def list_documents():
    return {
        "documents": [f for f in os.listdir(UPLOAD_DIR) if f.endswith('.pdf')],
        "total_chunks": len(vector_db.documents)
    }