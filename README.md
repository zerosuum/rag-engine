# Assignment 6 - RAG Engine

An end-to-end Retrieval-Augmented Generation (RAG) engine built with FastAPI, ChromaDB, and FastMCP. This system features an interactive Streamlit frontend, native text chunking, PDF extraction, and Model Context Protocol (MCP) integration for seamless communication with AI Agents.

## Project Structure
Adheres to standard Domain-Driven Design (DDD) modular architecture:
- `app/core` → Configuration & environment settings
- `app/repository` → Vector database persistence layer (ChromaDB)
- `app/services` → Business logic, native text chunking, and PDF text extraction
- `app/api` → REST API routing with pagination support
- `mcp` → FastMCP server acting as the "Robot Door" for AI Agent integration
- `frontend` → Interactive UI using Streamlit with custom aesthetic CSS cards

## How to Run

### 1. Install Dependencies
```bash
uv sync
```

### 2. Start the Backend Server
```bash
uv run uvicorn app.main:app --reload
```
The API will be available at http://127.0.0.1:8000/docs

### 3. Start the Frontend UI
```bash
uv run streamlit run frontend/app.py
```
The frontend web interface will open automatically in your browser.

### 4. Test the MCP Server
```bash
uv run mcp dev mcp/server.py
```
This will open the MCP Inspector to test the tools directly as an AI Agent.

## Test Scenarios

### 1. Document Upload & Extraction
- Open the Streamlit UI.
- Use the sidebar to upload a `.pdf` or `.txt` file containing specific information.
- The system will automatically extract, chunk, and store the embeddings in the local ChromaDB.

### 2. Semantic Search
- In the Streamlit UI Search Box, ask a contextual question based on the uploaded document.
- Example: "Apa masalah utama yang dihadapi Andi dan bagaimana solusinya?"
- The UI will render custom CSS cards showing the most relevant chunks along with their accuracy scores.

### 3. MCP Tool Call
- Inside the MCP Inspector, navigate to the `search_knowledge` tool.
- Input a query to let the AI agent retrieve real-time context from your local vector database.

## Features Overview
- Domain-Driven Design: Clean separation of concerns (API, Service, Repository).
- Zero-Cost Embeddings: Uses ChromaDB's native offline model (all-MiniLM-L6-v2), avoiding external API costs and rate limits
- Native Smart Chunking: Built-in text splitting with overlap parameters to preserve context.
- Multi-format Support: Directly processes PDF and TXT files.
- Clean UI: Microservice frontend using Streamlit with custom HTML/CSS rendering.
- MCP Ready: Exposes the RAG database as a tool for any MCP-compatible AI.

## Notes
- Upon the very first API execution, the system will download the local embedding model (~80MB). This may take a few seconds depending on your connection.
- The chroma_db/ directory stores your persistent local vector data and is safely ignored via .gitignore.