from langchain_openai import ChatOpenAI
from app.config import settings

class LLMService:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            api_key=settings.OPENAI_API_KEY,
            temperature=0.7
        )
    
    def summarize(self, text: str) -> str:
        prompt = f"Summarize the following text in 200 words:\n\n{text}"
        response = self.llm.invoke(prompt)
        return response.content
    
    def extract_keypoints(self, text: str) -> str:
        prompt = f"Extract 5 key points from the following text:\n\n{text}"
        response = self.llm.invoke(prompt)
        return response.content
    
    def answer_question(self, context: str, question: str) -> str:
        prompt = f"""Based on the following context, answer the question.\n\nContext:\n{context}\n\nQuestion: {question}\n\nAnswer:"""
        response = self.llm.invoke(prompt)
        return response.content

llm_service = LLMService()