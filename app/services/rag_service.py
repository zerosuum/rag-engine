import uuid
import io
from pypdf import PdfReader
from app.repository.chroma_store import get_repo

class RAGService:
    def __init__(self, repo_instance=get_repo()):
        self.repo = repo_instance

    def extract_text_from_file(self, file_bytes: bytes, filename: str) -> str:
        """Ekstrak teks dari PDF atau TXT"""
        if filename.lower().endswith(".pdf"):
            reader = PdfReader(io.BytesIO(file_bytes))
            text = ""
            for page in reader.pages:
                if page.extract_text():
                    text += page.extract_text() + "\n"
            return text
        else:
            return file_bytes.decode("utf-8", errors="ignore")

    def _chunk_text(self, text: str, words_per_chunk: int = 100, overlap: int = 20) -> list[str]:
        words = text.split()
        chunks = []
        for i in range(0, len(words), words_per_chunk - overlap):
            chunk = " ".join(words[i:i + words_per_chunk])
            chunks.append(chunk)
            if i + words_per_chunk >= len(words):
                break
        return chunks

    def add_document(self, text: str, metadata: dict | None = None) -> str:
        parent_doc_id = str(uuid.uuid4())
        base_meta = metadata or {"source": "api_upload"}
        
        chunks = self._chunk_text(text)
        
        for index, chunk_text in enumerate(chunks):
            chunk_id = f"{parent_doc_id}_chunk_{index}"
            
            chunk_meta = {
                **base_meta, 
                "parent_id": parent_doc_id, 
                "chunk_index": index
            }
            
            self.repo.add(chunk_id, chunk_text, chunk_meta)
            
        return parent_doc_id

    def get_all_documents(self) -> list:
        res = self.repo.get_all()
        if not res["ids"]:
            return []
        return [{"id": i, "metadata": m} for i, m in zip(res["ids"], res["metadatas"])]

    def get_document(self, doc_id: str) -> dict | None:
        chunk_id = f"{doc_id}_chunk_0"
        res = self.repo.get_by_id(chunk_id)
        if not res["ids"]:
            return None
        return {
            "id": res["ids"][0], 
            "text": res["documents"][0], 
            "metadata": res["metadatas"][0]
        }

    def search(self, query: str, n_results: int = 3) -> list:
        res = self.repo.search(query, n_results)
        if not res["ids"] or not res["ids"][0]:
            return []
        
        matches = []
        for i in range(len(res["ids"][0])):
            matches.append({
                "id": res["ids"][0][i],
                "text": res["documents"][0][i],
                "metadata": res["metadatas"][0][i],
                "distance": res["distances"][0][i]
            })
        return matches