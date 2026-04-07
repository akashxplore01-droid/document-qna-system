import faiss
import numpy as np
import pickle
from typing import List, Tuple

class FAISSVectorDB:
    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.documents = []
    
    def add_documents(self, embeddings: np.ndarray, documents: List[str]):
        self.index.add(embeddings.astype('float32'))
        self.documents.extend(documents)
    
    def search(self, query_embedding: np.ndarray, k: int = 4) -> Tuple[List[str], List[float]]:
        distances, indices = self.index.search(query_embedding.reshape(1, -1).astype('float32'), k)
        results = []
        scores = []
        for idx, distance in zip(indices[0], distances[0]):
            if idx < len(self.documents):
                results.append(self.documents[idx])
                scores.append(float(distance))
        return results, scores
    
    def save(self, path: str):
        faiss.write_index(self.index, f"{path}/index.faiss")
        with open(f"{path}/documents.pkl", "wb") as f:
            pickle.dump(self.documents, f)
    
    def load(self, path: str):
        self.index = faiss.read_index(f"{path}/index.faiss")
        with open(f"{path}/documents.pkl", "rb") as f:
            self.documents = pickle.load(f)

vector_db = FAISSVectorDB()