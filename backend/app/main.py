import os
from fastapi import FastAPI
from sqlalchemy import create_engine
from app.db.database import database, metadata
from app.api import chat

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL").replace("+asyncpg", "+psycopg2")
engine = create_engine(DATABASE_URL)
metadata.create_all(engine)

app.include_router(chat.router)

@app.get("/")
async def root():
    return {"message": "Mental Health Chatbot API", "version": "1.0.0"}

@app.on_event("startup")
async def connect_db():
    await database.connect()
    print("[INFO] Database connected")

@app.on_event("shutdown")
async def disconnect_db():
    await database.disconnect()
    print("[INFO] Database disconnected")
