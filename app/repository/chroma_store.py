import chromadb
from app.core.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChromaRepository:
    def __init__(self):
        logger.info(f"Initializing ChromaDB at {settings.CHROMA_PATH}")
        self.client = chromadb.PersistentClient(path=settings.CHROMA_PATH)

        self.collection = self.client.get_or_create_collection(
            name="rag_documents"
        )

    def add(self, doc_id: str, text: str, metadata: dict):
        self.collection.add(
            documents=[text], 
            metadatas=[metadata], 
            ids=[doc_id]
        )

    def get_all(self):
        return self.collection.get(include=["metadatas"])

    def get_by_id(self, doc_id: str):
        return self.collection.get(ids=[doc_id], include=["documents", "metadatas"])

    def search(self, query: str, n_results: int):
        return self.collection.query(
            query_texts=[query], 
            n_results=n_results, 
            include=["documents", "metadatas", "distances"]
        )

def get_repo():
    return ChromaRepository()