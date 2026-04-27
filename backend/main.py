from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

from services.processor import DocumentProcessor
from services.vector_store import VectorStore
from services.llm import LLMService

app = FastAPI(title="RAG Knowledge Assistant API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
processor = DocumentProcessor()
vector_store = VectorStore()
llm_service = LLMService()

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]

@app.post("/upload-document")
async def upload_document(file: UploadFile = File(...)):
    try:
        content = await file.read()
        chunks = processor.process_file(content, file.filename)
        # Clear previous document data to prevent 'Index Pollution'
        vector_store.clear()
        vector_store.add_chunks(chunks)
        return {"message": f"Successfully processed {len(chunks)} chunks from {file.filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask", response_model=QueryResponse)
async def ask_question(request: QueryRequest):
    try:
        # Step 1: Rewrite Query for better retrieval
        search_query = llm_service.rewrite_query(request.question)
        print(f"\nOriginal Question: {request.question}")
        print(f"Search Query: {search_query}")
        
        # Step 2: Search for relevant chunks using optimized query
        search_results = vector_store.search(search_query)
        if not search_results:
            print("No relevant chunks found.")
            return QueryResponse(answer="No documents uploaded or no relevant information found.", sources=[])
        
        context_chunks = [res[0] for res in search_results]
        print(f"Retrieved {len(context_chunks)} chunks.")
        for i, chunk in enumerate(context_chunks):
            print(f"--- Chunk {i+1} ---\n{chunk[:150]}...")
        
        # Step 3: Generate answer using LLM
        answer = llm_service.generate_answer(request.question, context_chunks)
        
        return QueryResponse(answer=answer, sources=context_chunks)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/clear")
async def clear_data():
    vector_store.clear()
    return {"message": "Data cleared successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
