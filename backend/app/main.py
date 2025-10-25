from fastapi import FastAPI
from sqlalchemy import create_engine
from app.db.database import database, DATABASE_URL, metadata
from app.api import chat

app = FastAPI()

engine = create_engine(DATABASE_URL.replace("+aiosqlite", ""))
metadata.create_all(engine)

app.include_router(chat.router)

@app.get("/")
async def root():
    return {"message": "Mental Health Chatbot API", "version": "1.0.0"}

@app.on_event("startup")
async def connect_db():
    await database.connect()

@app.on_event("shutdown")
async def disconnect_db():
    await database.disconnect()
