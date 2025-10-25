from app.db.database import database
from app.db.models import Message, Conversation

async def create_message(conversation_id: int, sender: str, content: str):
  query = Message.__table__.insert().values(
    conversation_id=conversation_id,
    role=sender,
    content=content
  )
  message_id = await database.execute(query)

  return message_id

async def get_messages(conversation_id: int):
  query = Message.__table__.select().where(Message.__table__.c.conversation_id == conversation_id)

  return await database.fetch_all(query)


async def create_conversation():
  query = Conversation.__table__.insert().values()
  conversation_id = await database.execute(query)

  return conversation_id

async def get_conversations():
  query = Conversation.__table__.select()

  return await database.fetch_all(query)
