import sys
import os
from sqlalchemy import create_engine, text

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL").replace("+asyncpg", "+psycopg2")
engine = create_engine(DATABASE_URL)

def enforce_not_null():
    with engine.connect() as conn:
        print("Enforcing NOT NULL constraint on conversations.user_id...")
        
        try:
            # Check if there are any nulls left (shouldn't be if we ran the link script)
            result = conn.execute(text("SELECT COUNT(*) FROM conversations WHERE user_id IS NULL"))
            count = result.scalar()
            
            if count > 0:
                print(f"ERROR: Found {count} conversations with NULL user_id. Cannot enforce constraint.")
                print("Please run link_conversations_to_user.py first or handle these records.")
                return

            conn.execute(text("ALTER TABLE conversations ALTER COLUMN user_id SET NOT NULL"))
            conn.commit()
            print("Successfully enforced NOT NULL constraint on user_id.")
        except Exception as e:
            print(f"Error enforcing constraint: {e}")

if __name__ == "__main__":
    enforce_not_null()
