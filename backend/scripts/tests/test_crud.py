import sys
import os
import asyncio

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.database import database
from app.db.crud import create_conversation

async def test_create_conversation():
    try:
        await database.connect()
        print("Connected to DB")
        
        print("Attempting to create conversation...")
        conversation_id = await create_conversation()
        print(f"Success! Conversation ID: {conversation_id}")
        
        await database.disconnect()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_create_conversation())
