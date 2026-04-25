import os
from groq import Groq
from dotenv import load_dotenv
from typing import List

load_dotenv()

class LLMService:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        self.client = Groq(api_key=api_key)
        self.model = os.getenv("MODEL_NAME", "llama3-8b-8192")

    def rewrite_query(self, user_query: str) -> str:
        """Rewrites a vague user query into a search-optimized query."""
        prompt = f"""
        Transform the following user question into a clear, descriptive search query that will help find relevant information in a vector database.
        Focus on identifying the core entities and intent.
        
        USER QUESTION: {user_query}
        SEARCH OPTIMIZED QUERY:
        """
        response = self.client.chat.completions.create(
            messages=[{"role": "system", "content": "You are a search optimization assistant."},
                      {"role": "user", "content": prompt}],
            model=self.model,
            temperature=0,
        )
        return response.choices[0].message.content.strip()

    def generate_answer(self, query: str, context_chunks: List[str]) -> str:
        context = "\n\n".join([f"[Chunk {i+1}]: {c}" for i, c in enumerate(context_chunks)])
        prompt = f"""
        You are an expert AI analysis assistant. Use the provided context chunks to answer the user's question.
        
        RULES:
        1. Answer ONLY using the provided context.
        2. If the answer requires combining information from multiple chunks, do so carefully.
        3. If the information is not present, say: "I'm sorry, but I couldn't find sufficient information in the uploaded document to answer that."
        4. Be precise, professional, and grounded. Do not hallucinate or use outside knowledge.
        
        CONTEXT:
        {context}
        
        QUESTION:
        {query}
        
        DETAILED ANSWER:
        """
        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a specialized RAG assistant that synthesizes information from multiple context sources."},
                {"role": "user", "content": prompt}
            ],
            model=self.model,
            temperature=0.2,
        )
        return response.choices[0].message.content
