from dotenv import load_dotenv
import os
from groq import Groq
from app.config import LLM_MODEL_NAME

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

def get_answer_from_llm(question,context):
    prompt = f"Context:\n{context}\n\nQuestion: {question}\n\nAnswer based only on the context above."

    response = client.chat.completions.create(
        model=LLM_MODEL_NAME,
        messages=[
            {"role":"user","content":prompt}
        ]
    )

    answer=response.choices[0].message.content
    return answer



