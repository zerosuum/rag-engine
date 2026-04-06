import sys
import os
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp.server.fastmcp import FastMCP
from app.services.rag_service import RAGService

mcp = FastMCP("RAG Server")
rag_service = RAGService()

# 1. Tools
@mcp.tool()
def upload_knowledge(text: str, source: str = "mcp_agent") -> dict:
    """Upload text into the RAG Vector Database for future reference."""
    doc_id = rag_service.add_document(text, {"source": source})
    return {
        "status": "success",
        "action": "document_uploaded",
        "doc_id": doc_id
    }

@mcp.tool()
def search_knowledge(query: str) -> dict:
    """Semantic search to find relevant information from the RAG database."""
    results = rag_service.search(query)
    if not results:
        return {"status": "success", "results": [], "message": "No relevant documents found."}
    
    return {
        "status": "success",
        "query": query,
        "total_found": len(results),
        "results": [{"text": res['text'], "relevance_score": res['distance']} for res in results]
    }

@mcp.tool()
def list_all_knowledge() -> dict:
    """Retrieve a list of all document metadata currently stored in the RAG database."""
    docs = rag_service.get_all_documents()
    return {
        "status": "success",
        "total_documents": len(docs),
        "documents": docs
    }

@mcp.tool()
def get_knowledge_details(doc_id: str) -> dict:
    """Retrieve the full text and metadata of a specific document using its ID."""
    doc = rag_service.get_document(doc_id)
    if not doc:
        return {"status": "error", "message": f"Document with ID {doc_id} not found."}
    return {
        "status": "success",
        "document": doc
    }

# 2. Resources
@mcp.resource("rag://system_status")
def get_system_status() -> str:
    """Read the real-time health and status of the RAG Vector Database."""
    docs = rag_service.get_all_documents()
    status = {
        "status": "healthy",
        "total_documents_in_db": len(docs),
        "database_type": "ChromaDB Local Persistent",
        "architecture": "Modular DDD"
    }
    return json.dumps(status, indent=2)

# 3. Prompts
@mcp.prompt("deep_document_analysis")
def deep_analysis_prompt(query_topic: str) -> str:
    """Command the AI to deeply analyze a topic using the RAG database."""
    return (
        f"Gunakan tool `search_knowledge` untuk mencari informasi tentang '{query_topic}' "
        "di dalam RAG Database internal. Berikan rangkuman komprehensif berdasarkan "
        "data yang dikembalikan oleh tool. Jika datanya kosong, laporkan bahwa pengetahuan belum ada."
    )

if __name__ == "__main__":
    mcp.run()