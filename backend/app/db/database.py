from sqlalchemy import MetaData
from databases import Database

DATABASE_URL = "sqlite+aiosqlite:///./chatbot.db"

database = Database(DATABASE_URL)

metadata = MetaData()
