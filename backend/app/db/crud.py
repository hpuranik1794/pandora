from app.db.database import database
from app.db.models import Message, Conversation
from app.services.embedding import embed_text
from sqlalchemy import select, func

async def next_turn_id(conversation_id: int) -> int:
  q = select(func.coalesce(func.max(Message.turn_id), 0)).where(Message.conversation_id == conversation_id)
  last = await database.fetch_val(q)
  return int(last) + 1


async def create_message(conversation_id: int, user_input: str, response: str):
  turn_id = await next_turn_id(conversation_id)

  user_embedding = await embed_text(user_input)
  
  await database.execute(Message.__table__.insert().values(
    conversation_id=conversation_id,
    turn_id=turn_id,
    role="user",
    content=user_input,
    embedding=user_embedding
  ))

  await database.execute(Message.__table__.insert().values(
    conversation_id=conversation_id,
    turn_id=turn_id,
    role="assistant",
    content=response
  ))
  
  return turn_id

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
