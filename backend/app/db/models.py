from sqlalchemy import Table, Column, Integer, String, Text, DateTime, CheckConstraint, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from app.db.database import metadata

Base = declarative_base(metadata=metadata)

class Message(Base):
  __tablename__ = "messages"

  id = Column(Integer, primary_key=True, autoincrement=True)
  conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
  role = Column(String(50), CheckConstraint("role IN ('user', 'assistant')"), nullable=False)
  content = Column(Text, nullable=False)
  timestamp = Column(DateTime, server_default=func.now())

class Conversation(Base):
  __tablename__ = "conversations"

  id = Column(Integer, primary_key=True, autoincrement=True)
  created_at = Column(DateTime, server_default=func.now())
    
