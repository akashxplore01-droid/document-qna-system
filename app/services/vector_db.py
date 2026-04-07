import numpy as np
import faiss

def compute_inner_product(a, b):
    return np.dot(a, b)

class FAISSVectorDB:
    def __init__(self, dimension):
        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension)  # Inner Product index
        self.embeddings = []

    def add_embeddings(self, embeddings):
        if embeddings.shape[1] != self.dimension:
            raise ValueError(f"Embeddings must have dimension {self.dimension}")
        self.index.add(embeddings)
        self.embeddings.extend(embeddings)

    def search(self, query, k=5):
        distances, indices = self.index.search(query, k)
        return distances, indices

    def save(self, file_path):
        faiss.write_index(self.index, file_path)

    @classmethod
    def load(cls, file_path):
        index = faiss.read_index(file_path)
        instance = cls(index.d)
        instance.index = index
        return instance
