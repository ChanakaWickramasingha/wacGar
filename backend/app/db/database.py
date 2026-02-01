from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL) #connected with postgreSQL
SessionLocal = sessionmaker(bind=engine) # talk to DB
Base = declarative_base() #parent for table
