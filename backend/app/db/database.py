from sqlalchemy import MetaData
from databases import Database
from dotenv import load_dotenv
import os

load_dotenv()

database = Database(os.getenv("DATABASE_URL"))

metadata = MetaData()
