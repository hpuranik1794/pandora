import sys
import os

# Add the parent directory to sys.path to allow importing from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from app.db.models import Base, Conversation, Message


sqlite_engine = create_engine("sqlite:///../chatbot.db", echo=False)
url = URL.create(
  drivername="postgresql+psycopg2",
  username="pandora",
  password="root",
  host="localhost",
  port=5433,
  database="pandora"
)
pg_engine = create_engine(url)

SQLiteSession = sessionmaker(bind=sqlite_engine)
PGSession = sessionmaker(bind=pg_engine)

sqlite_session = SQLiteSession()
pg_session = PGSession()


Base.metadata.create_all(pg_engine)


def migrate_data():
  print("Reading SQLite conversations...")
  conversations = sqlite_session.query(Conversation).all()

  for conv in conversations:
    new_conv = Conversation(
      id=conv.id,
      created_at=conv.created_at
    )
    pg_session.add(new_conv)

    
    msgs = (
      sqlite_session.query(Message)
      .filter(Message.conversation_id == conv.id)
      .order_by(Message.turn_id.asc())
      .all()
    )

    for msg in msgs:
      new_msg = Message(
        id=msg.id,
        conversation_id=new_conv.id,
        turn_id=msg.turn_id,
        role=msg.role,
        content=msg.content,
        embedding=msg.embedding,
        timestamp=msg.timestamp
      )
      pg_session.add(new_msg)

    print(f"Migrated conversation {conv.id} with {len(msgs)} messages")

  pg_session.commit()

if __name__ == "__main__":
  migrate_data()
