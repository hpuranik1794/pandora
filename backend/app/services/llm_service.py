from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(base_url=os.getenv("BASE_URL"), api_key=os.getenv("API_KEY"))

async def generate_response(user_input: str) -> str:
  messages = [
    {"role": "system", "content": "You are a compassionate mental health assistant."},
    {"role": "user", "content": user_input}
  ]

  response = client.chat.completions.create(
    model=os.getenv("MODEL_NAME"),
    messages=messages
  )

  return response.choices[0].message.content

async def generate_embedding(text: str) -> list:
  pass  # Embedding generation not implemented yet
