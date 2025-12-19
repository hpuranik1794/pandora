from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(base_url=os.getenv("BASE_URL"), api_key=os.getenv("API_KEY"))

def build_prompt(user_input, context_messages):
  context_text = "\n".join(context_messages)

  return f"""
    You are a compassionate mental health assistant.
    Here are some past messages for context:
    {context_text}

    User: {user_input}
    Assistant:
  """

async def generate_response(user_input: str, context_messages: list) -> str:
  prompt = build_prompt(user_input, context_messages)
  messages = [
    {"role": "system", "content": "You are a compassionate mental health assistant. Be supportive and understanding but also restrict your response to no more than 50 words."},
    {"role": "user", "content": prompt}
  ]

  response = client.chat.completions.create(
    model=os.getenv("MODEL_NAME"),
    messages=messages
  )

  return response.choices[0].message.content


