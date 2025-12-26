import sys
import os
import asyncio

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.database import database
from app.services.embedding import get_relevant_messages

async def test_rag():
  try:
    await database.connect()
    print("Connected to DB")
    
    conversation_id = 3
    query = "I feel very anxious about my job."
    print(f"Query: {query}")
    
    context_messages = await get_relevant_messages(conversation_id, query, top_k=2)
    
    print(f"\nFound {len(context_messages)} total context messages:")
    for msg in context_messages:
      source = msg.get("source", "unknown")
      role = msg["role"]
      content_preview = msg["content"][:100].replace('\n', ' ')
      print(f"[{source.upper()}] {role}: {content_preview}...")
        
    await database.disconnect()
  except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

if __name__ == "__main__":
  asyncio.run(test_rag())
