import openai

class LLMService:
    def __init__(self, api_key):
        openai.api_key = api_key

    def summarize(self, text):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"Please summarize the following text: {text}"}]
        )
        return response['choices'][0]['message']['content']

    def extract_key_points(self, text):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"Please extract key points from the following text: {text}"}]
        )
        return response['choices'][0]['message']['content']

    def answer_question(self, question, context):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"Using the context: {context}, answer the question: {question}"}]
        )
        return response['choices'][0]['message']['content']
