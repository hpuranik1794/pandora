import sys
import os
import asyncio

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.database import database
from app.db.crud import create_message

async def test_create_message():
    try:
        await database.connect()
        print("Connected to DB")
        
        # Assuming conversation_id 4 exists from previous test
        conversation_id = 4 
        print(f"Attempting to create message for conversation {conversation_id}...")
        
        turn_id = await create_message(conversation_id, "Hello", "Hi there!")
        print(f"Success! Turn ID: {turn_id}")
        
        await database.disconnect()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_create_message())
