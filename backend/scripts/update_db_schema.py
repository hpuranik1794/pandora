import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL").replace("+asyncpg", "+psycopg2")
engine = create_engine(DATABASE_URL)

from app.db.models import Base

def update_schema():
  print("Creating new tables if they don't exist...")
  Base.metadata.create_all(engine)
  
  with engine.connect() as conn:
    print("Checking schema updates...")
    
    try:
      print("Attempting to add user_id column to conversations table...")
      conn.execute(text("ALTER TABLE conversations ADD COLUMN IF NOT EXISTS user_id INTEGER REFERENCES users(id)"))
      conn.commit()
      print("Successfully added user_id column (or it already existed).")
    except Exception as e:
      print(f"Error adding column: {e}")

if __name__ == "__main__":
  update_schema()
