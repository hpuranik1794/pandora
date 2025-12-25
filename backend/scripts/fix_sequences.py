import sys
import os
import asyncio
from sqlalchemy import text

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.database import database

async def fix_sequences():
    try:
        await database.connect()
        print("Connected to DB")
        
        # Fix conversations sequence
        print("Fixing conversations sequence...")
        await database.execute(text("SELECT setval('conversations_id_seq', COALESCE((SELECT MAX(id) FROM conversations), 0) + 1, false);"))
        
        # Fix messages sequence
        print("Fixing messages sequence...")
        
        # Get the sequence name dynamically
        seq_name_query = text("SELECT pg_get_serial_sequence('messages', 'id')")
        seq_name = await database.fetch_val(seq_name_query)
        
        if seq_name:
            print(f"Found sequence name: {seq_name}")
            # seq_name might be 'public.messages_id_seq' or similar
            await database.execute(text(f"SELECT setval('{seq_name}', COALESCE((SELECT MAX(id) FROM messages), 0) + 1, false);"))
        else:
            print("Could not find sequence name for messages.id, trying default 'messages_id_seq'")
            await database.execute(text("SELECT setval('messages_id_seq', COALESCE((SELECT MAX(id) FROM messages), 0) + 1, false);"))
        
        print("Sequences updated successfully.")
        
        await database.disconnect()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(fix_sequences())
