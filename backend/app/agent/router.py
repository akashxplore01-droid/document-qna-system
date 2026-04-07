from app.services.cache import cache_service
from app.services.llm import llm_service
from app.services.vector_db import vector_db
from app.services.embeddings import embedding_service

class AgentRouter:
    def __init__(self):
        self.tools = {
            'summary': self.handle_summary,
            'key points': self.handle_keypoints,
            'keypoints': self.handle_keypoints,
            'book name': self.handle_book_name,
            'rag': self.handle_rag
        }
    
    def route(self, query: str, context: str = ""):
        cached = cache_service.get_cached_answer(query)
        if cached:
            return {
                'answer': cached['answer'],
                'tool': 'cache',
                'source': 'cache'
            }
        
        query_lower = query.lower()
        
        if 'summary' in query_lower or 'summarize' in query_lower:
            answer = llm_service.summarize(context)
            tool = 'summary'
        elif 'key point' in query_lower or 'keypoint' in query_lower:
            answer = llm_service.extract_keypoints(context)
            tool = 'keypoints'
        elif 'book name' in query_lower or 'title' in query_lower:
            answer = llm_service.answer_question(context, query)
            tool = 'book_name'
        else:
            results, scores = vector_db.search(embedding_service.get_embedding(query), k=4)
            context = "\n".join(results)
            answer = llm_service.answer_question(context, query)
            tool = 'rag'
        
        cache_service.cache_answer(query, answer, tool)
        
        return {
            'answer': answer,
            'tool': tool,
            'source': 'agent'
        }
    
    def handle_summary(self, text: str):
        return llm_service.summarize(text)
    
    def handle_keypoints(self, text: str):
        return llm_service.extract_keypoints(text)
    
    def handle_book_name(self, text: str):
        return llm_service.answer_question(text, "What is the name/title of this document?")
    
    def handle_rag(self, query: str):
        results, _ = vector_db.search(embedding_service.get_embedding(query), k=4)
        context = "\n".join(results)
        return llm_service.answer_question(context, query)

agent_router = AgentRouter()