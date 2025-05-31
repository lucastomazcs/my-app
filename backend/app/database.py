# backend/app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
print(f"DEBUG: DATABASE_URL sendo usada pela aplicação = {DATABASE_URL}")
if not DATABASE_URL:
    print("ERRO CRÍTICO: A variável de ambiente DATABASE_URL não está definida!")


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False)
Base = declarative_base()