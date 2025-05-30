from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from .database import Base
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class TokenBlocklist(Base):
    __tablename__ = "token_blocklist"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True, nullable=False)
    token_type = Column(String, nullable=False)  # "access" ou "refresh"
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    revoked = Column(Boolean, default=False)

    user = relationship("User", back_populates="tokens")

User.tokens = relationship("TokenBlocklist", back_populates="user")


class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    quantity = Column(Integer, default=0, nullable=False)
