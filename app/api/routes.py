from fastapi import APIRouter, HTTPException, Query, UploadFile, File
from pydantic import BaseModel, Field
from app.services.rag_service import RAGService
from typing import Optional

router = APIRouter()
rag_service = RAGService()

class DocumentInput(BaseModel):
    text: str = Field(..., min_length=1, description="Document content")
    metadata: Optional[dict] = None

class SearchQuery(BaseModel):
    query: str = Field(..., min_length=1, description="Search keyword")
    n_results: int = Field(3, ge=1, le=20, description="Max results to return") # <-- Kasih limit biar gak jebol

@router.get("/health", summary="System Health Check")
def health_check():
    return {"status": "ok", "service": "RAG API Layer"}

@router.post("/documents", summary="Upload Dokumen")
def upload_document(doc: DocumentInput):
    if not doc.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")
    
    doc_id = rag_service.add_document(doc.text, doc.metadata)
    return {"message": "Document chunked and added successfully", "parent_id": doc_id}

@router.post("/documents/file", summary="Upload Dokumen File (PDF/TXT)")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    text = rag_service.extract_text_from_file(content, file.filename or "")
    
    if not text.strip():
        raise HTTPException(status_code=400, detail="Teks tidak terbaca dari file ini.")
    
    doc_id = rag_service.add_document(text, {"filename": file.filename})
    return {"message": f"File {file.filename} berhasil diproses", "parent_id": doc_id}

@router.get("/documents", summary="Get Semua Dokumen (with Pagination)")
def list_documents(
    skip: int = Query(0, description="Jumlah data yang dilewati"), 
    limit: int = Query(10, description="Maksimal data yang diambil")
):
    all_docs = rag_service.get_all_documents()

    paginated_docs = all_docs[skip : skip + limit]
    
    return {
        "total_chunks_in_db": len(all_docs),
        "showing": len(paginated_docs),
        "documents": paginated_docs
    }

@router.get("/documents/{doc_id}", summary="Get Dokumen by ID")
def get_document(doc_id: str):
    doc = rag_service.get_document(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc

@router.post("/search", summary="Semantic Search RAG")
def semantic_search(search: SearchQuery):
    if not search.query.strip():
        raise HTTPException(status_code=400, detail="Search query cannot be empty.")
        
    results = rag_service.search(search.query, search.n_results)
    return {"results": results}