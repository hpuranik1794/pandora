from fastapi import FastAPI
from app.api import chat

app = FastAPI()

app.include_router(chat.router)

@app.get("/")
async def root():
    return {"message": "Mental Health Chatbot API", "version": "1.0.0"}
