from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os 
from dotenv import load_dotenv
load_dotenv()
Base=declarative_base()

DATABASE_URL=os.getenv("DATABASE_URL")
if DATABASE_URL:
    # Mask password for security: postgresql://user:PASSWORD@host:port/db
    masked_url = DATABASE_URL
    if "@" in DATABASE_URL and ":" in DATABASE_URL.split("@")[0][11:]:
        prefix, rest = DATABASE_URL.split("@")
        protocol_user, pwd = prefix.rsplit(":", 1)
        masked_url = f"{protocol_user}:****@{rest}"
    print("DATABASE_URL", masked_url)

engine=create_engine(DATABASE_URL)
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()