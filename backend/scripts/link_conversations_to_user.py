import sys
import os
import asyncio

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.database import database
from app.db.models import User, Conversation
from sqlalchemy import select, update

async def link_conversations():
    await database.connect()
    try:
        username = "yo"
        print(f"Looking for user '{username}'...")
        
        query = select(User).where(User.username == username)
        user = await database.fetch_one(query)
        
        if not user:
            print(f"User '{username}' not found!")
            return

        user_id = user.id
        print(f"Found user '{username}' with ID: {user_id}")
        
        print("Linking unlinked conversations to this user...")
        
        # Update conversations where user_id is NULL
        update_query = (
            update(Conversation)
            .where(Conversation.user_id == None)
            .values(user_id=user_id)
        )
        
        await database.execute(update_query)
        print("Conversations linked successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await database.disconnect()

if __name__ == "__main__":
    asyncio.run(link_conversations())
