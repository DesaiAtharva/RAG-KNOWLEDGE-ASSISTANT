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
        context = "\n\n".join(context_chunks)
        
        system_prompt = """
        You are a strict RAG Assistant. Your answers must be precise, grounded, and professional.
        
        STRICT RULES:
        1. Direct Answers: Do NOT use phrases like "Based on the context," "It appears," "Likely," or "According to the document." Just state the fact.
        2. NO HEDGING: Do not guess, infer, or provide outside knowledge.
        3. Length: Keep your answer to 2-3 sentences maximum. No long paragraphs.
        4. Not Found: If the information is not explicitly in the provided text, you MUST say exactly: "Not found in the document."
        5. Formatting: Use bold text for key terms.
        """
        
        user_prompt = f"""
        Information:
        {context}

        Question:
        {query}

        Instruction: 
        Answer the question directly in 2-3 sentences using ONLY the provided information. If not found, say "Not found in the document."
        """
        
        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model=self.model,
            temperature=0, # Maximum grounding/precision
        )
        return response.choices[0].message.content
