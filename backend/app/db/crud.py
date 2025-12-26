from sqlalchemy import select, func, text
from app.db.database import database
from app.db.models import Message, Conversation, User
from app.services.embedding import embed_text
from app.services.security import encrypt_content, decrypt_content

async def next_turn_id(conversation_id: int) -> int:
  q = select(func.coalesce(func.max(Message.turn_id), 0)).where(Message.conversation_id == conversation_id)
  last = await database.fetch_val(q)
  return int(last) + 1


async def create_message(conversation_id: int, user_input: str, response: str):
  turn_id = await next_turn_id(conversation_id)

  user_embedding = await embed_text(user_input)
  
  # Encrypt user content
  encrypted_user_input = encrypt_content(user_input)
  
  await database.execute(Message.__table__.insert().values(
    conversation_id=conversation_id,
    turn_id=turn_id,
    role="user",
    content=encrypted_user_input,
    embedding=user_embedding
  ).returning(Message.id))

  # Encrypt assistant response
  encrypted_response = encrypt_content(response)

  await database.execute(Message.__table__.insert().values(
    conversation_id=conversation_id,
    turn_id=turn_id,
    role="assistant",
    content=encrypted_response
  ).returning(Message.id))
  
  return turn_id

async def get_messages(conversation_id: int):
  query = Message.__table__.select().where(Message.__table__.c.conversation_id == conversation_id)
  rows = await database.fetch_all(query)
  
  # Decrypt content
  decrypted_rows = []
  for row in rows:
    row_dict = dict(row)
    row_dict["content"] = decrypt_content(row_dict["content"])
    decrypted_rows.append(row_dict)
      
  return decrypted_rows


async def create_conversation(user_id: int):
  query = Conversation.__table__.insert().values(user_id=user_id).returning(Conversation.id)
  conversation_id = await database.fetch_val(query)

  return conversation_id


async def get_conversations(user_id: int):
  query = Conversation.__table__.select().where(Conversation.user_id == user_id).order_by(Conversation.created_at.asc())

  return await database.fetch_all(query)


async def get_conversation(conversation_id: int):
  query = Conversation.__table__.select().where(Conversation.id == conversation_id)

  return await database.fetch_one(query)


async def create_user(user: dict):
  query = User.__table__.insert().values(
    username=user["username"],
    hashed_password=user["hashed_password"]
  )
  
  return await database.execute(query)


async def get_user(username: str):
  query = User.__table__.select().where(User.username == username)
  return await database.fetch_one(query)
