from sqlalchemy import Column, Integer, String, Text, DateTime, CheckConstraint, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
from app.db.database import metadata

Base = declarative_base(metadata=metadata)

class RagMessage(Base):
  __tablename__ = "rag_messages"

  id = Column(Integer, primary_key=True, autoincrement=True)
  turn_id = Column(Integer, nullable=False)
  role = Column(String(50), CheckConstraint("role IN ('user', 'assistant')"), nullable=False)
  content = Column(Text, nullable=False)
  embedding = Column(JSON, nullable=True)
  embedding_vec = Column(Vector(1024), nullable=True)
  timestamp = Column(DateTime, server_default=func.now())


class Message(Base):
  __tablename__ = "messages"

  id = Column(Integer, primary_key=True, autoincrement=True)
  conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
  turn_id = Column(Integer, nullable=False)
  role = Column(String(50), CheckConstraint("role IN ('user', 'assistant')"), nullable=False)
  content = Column(Text, nullable=False)
  embedding = Column(JSON, nullable=True)
  timestamp = Column(DateTime, server_default=func.now())


class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True, autoincrement=True)
  username = Column(String(50), unique=True, nullable=False)
  hashed_password = Column(String(255), nullable=False)
  created_at = Column(DateTime, server_default=func.now())

class Conversation(Base):
  __tablename__ = "conversations"

  id = Column(Integer, primary_key=True, autoincrement=True)
  user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
  created_at = Column(DateTime, server_default=func.now())
    
