import os
from sqlalchemy import create_engine, inspect
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
inspector = inspect(engine)
tables = inspector.get_table_names()
print("Existing tables:", tables)

if "chat_history" in tables:
    print("chat_history table exists.")
else:
    print("chat_history table MISSING!")

if "chat_messages" in tables:
    print("chat_messages table exists.")
else:
    print("chat_messages table MISSING!")
