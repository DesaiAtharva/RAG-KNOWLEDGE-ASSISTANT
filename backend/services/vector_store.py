import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Tuple
import os
from dotenv import load_dotenv

load_dotenv()

class VectorStore:
    def __init__(self):
        model_name = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
        self.index = faiss.IndexFlatL2(self.dimension)
        self.chunks = []

    def add_chunks(self, chunks: List[str]):
        if not chunks:
            return
        embeddings = self.model.encode(chunks)
        self.index.add(np.array(embeddings).astype("float32"))
        self.chunks.extend(chunks)

    def search(self, query: str, top_k: int = 4) -> List[Tuple[str, float]]:
        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(np.array(query_embedding).astype("float32"), top_k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1 and idx < len(self.chunks):
                results.append((self.chunks[idx], float(distances[0][i])))
        return results

    def clear(self):
        self.index = faiss.IndexFlatL2(self.dimension)
        self.chunks = []
