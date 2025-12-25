from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, CheckConstraint, JSON
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func
from sqlalchemy import select
from pgvector.sqlalchemy import Vector
from services.embedding import embed_text
import pandas as pd
import asyncio


url = URL.create(
  drivername="postgresql+psycopg2",
  username="pandora",
  password="root",
  host="localhost",
  port=5433,
  database="pandora"
)
engine = create_engine(url)
connection = engine.connect()

Base = declarative_base()

class RagMessage(Base):
  __tablename__ = "rag_messages"

  id = Column(Integer, primary_key=True, autoincrement=True)
  turn_id = Column(Integer, nullable=False)
  role = Column(String(50), CheckConstraint("role IN ('user', 'assistant')"), nullable=False)
  content = Column(Text, nullable=False)
  embedding = Column(JSON, nullable=True)
  embedding_vec = Column(Vector(1024), nullable=True)
  timestamp = Column(DateTime, server_default=func.now())

Base.metadata.create_all(engine)


async def load_data(df: pd.DataFrame):
  Session = sessionmaker(bind=engine)
  session = Session()

  for i, row in df.iterrows():
    context = row["Context"]
    context_embd = await embed_text(context)

    response = row["Response"]
    response_embd = await embed_text(response)

    print(f"Loading data {i}...")
    session.add_all([
      RagMessage(
        turn_id=(i+1),
        role="user",
        content=context,
        embedding=context_embd
      ),

      RagMessage(
        turn_id=(i+1),
        role="assistant",
        content=response,
        embedding=response_embd
      )
    ])

    session.commit()

  print(session.query(RagMessage.content, RagMessage.embedding)[0])
  print(session.query(RagMessage.content, RagMessage.embedding)[0])

  session.close()


def update_embeddings():
  Session = sessionmaker(bind=engine)
  session = Session()

  messages = session.query(Message).filter(Message.embedding != None).all()

  for msg in messages:
    try:
      msg.embedding_vec = msg.embedding
      session.commit()
      print(f"Saved embedding for message {msg.id}")

    except ValueError as e:
      print(f"Skipping message {msg.id} due to dimension error: {e}")
      session.rollback()

    except Exception as e:
      print(f"Unexpected error msg {msg.id}: {e}")
      session.rollback()

  session.close()



if __name__ == "__main__":
  # df = pd.read_json("hf://datasets/Amod/mental_health_counseling_conversations/combined_dataset.json", lines=True)
  # asyncio.run(load_data(df))
  update_embeddings()


