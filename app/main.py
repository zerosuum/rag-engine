from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="RAG Engine API",
    description="Backend service separating Human REST API and AI MCP Server interfaces.",
    version="1.0.0"
)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)