from openai import OpenAI
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
import os

load_dotenv()

client = OpenAI(base_url=os.getenv("BASE_URL"), api_key=os.getenv("API_KEY"))

app = FastAPI()


@app.post("/chat")
async def chat_response(request: Request):
  try:
    user_input = await request.json()
    messages = [
      {"role": "system", "content": "You are a compassionate mental health assistant."},
      {"role": "user", "content": user_input["user_input"]}
    ]

    response = client.chat.completions.create(
      model=os.getenv("MODEL_NAME"),
      messages=messages
    )

    return {"response": response.choices[0].message.content}
  
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
