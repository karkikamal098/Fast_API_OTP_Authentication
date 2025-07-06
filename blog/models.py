from .database import Base
from sqlalchemy import Column, Integer, String

class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, default=None, primary_key=True, index=True)
    title = Column(String, index=True)
    body = Column(String, index=True)



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, default=None, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    name = Column(String, index=True)

    