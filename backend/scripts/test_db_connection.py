import sys
import os
import asyncio

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.database import database

async def test_connection():
  try:
    await database.connect()
    print("Successfully connected to PostgreSQL!")
    await database.disconnect()
  except Exception as e:
    print(f"Failed to connect: {e}")

if __name__ == "__main__":
  asyncio.run(test_connection())
