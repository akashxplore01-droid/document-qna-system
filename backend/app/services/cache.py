import redis
import json
import numpy as np
from app.services.embeddings import embedding_service
from app.config import settings

class RedisCache:
    def __init__(self):
        try:
            self.client = redis.from_url(settings.REDIS_URL)
            self.client.ping()
        except Exception as e:
            print(f"Redis connection failed: {e}. Cache will be disabled.")
            self.client = None
    
    def get_cached_answer(self, query: str, threshold: float = 0.85) -> dict:
        if not self.client:
            return None
        
        query_embedding = embedding_service.get_embedding(query)
        
        try:
            keys = self.client.keys("query:*")
            for key in keys:
                cached_data = self.client.get(key)
                if cached_data:
                    cached_data = json.loads(cached_data)
                    cached_embedding = np.array(cached_data['embedding'])
                    similarity = embedding_service.cosine_similarity(query_embedding, cached_embedding)
                    if similarity >= threshold:
                        return cached_data
        except Exception as e:
            print(f"Cache retrieval error: {e}")
        
        return None
    
    def cache_answer(self, query: str, answer: str, tool_used: str):
        if not self.client:
            return
        
        try:
            query_embedding = embedding_service.get_embedding(query)
            cache_data = {
                'query': query,
                'answer': answer,
                'tool_used': tool_used,
                'embedding': query_embedding.tolist()
            }
            key = f"query:{hash(query)}"
            self.client.setex(key, 86400, json.dumps(cache_data))
        except Exception as e:
            print(f"Cache storage error: {e}")

cache_service = RedisCache()