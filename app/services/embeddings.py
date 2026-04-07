from sentence_transformers import SentenceTransformer, util

class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def get_embeddings(self, texts):
        return self.model.encode(texts, convert_to_tensor=True)

    def cosine_similarity(self, embedding1, embedding2):
        return util.pytorch_cos_sim(embedding1, embedding2).
