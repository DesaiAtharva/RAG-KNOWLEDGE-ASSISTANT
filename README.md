# RAG Knowledge Assistant 🚀

An intelligent AI system that accepts documents (PDF/Text), understands their content, and answers user queries based strictly on the provided knowledge.

## Features
- **Advanced RAG Pipeline**: Uses local embeddings (`sentence-transformers`) and FAISS for fast retrieval.
- **Query Rewriting**: Intelligently optimizes user questions for better semantic search.
- **Knowledge Grounding**: Strict prompt engineering to prevent hallucinations.
- **Premium UI**: Built with Next.js featuring a glassmorphic dark-mode interface.

## Tech Stack
- **Backend**: FastAPI, PyPDF2, FAISS, Sentence-Transformers, Groq LLM.
- **Frontend**: Next.js (App Router), Vanilla CSS.

## Getting Started

### Backend Setup
1. Navigate to `backend/`.
2. Install dependencies: `pip install -r requirements.txt`.
3. Create a `.env` file with your `GROQ_API_KEY`.
4. Run the server: `python main.py`.

### Frontend Setup
1. Navigate to `frontend/`.
2. Install dependencies: `npm install`.
3. Run the dev server: `npm run dev`.

## Implementation Details
This project demonstrates the transition from Basic RAG to Advanced RAG by implementing:
- Micro-chunking (300 chars / 50 overlap)
- Deep retrieval (top-k=7)
- Semantic query rewriting
- Structured context injection
