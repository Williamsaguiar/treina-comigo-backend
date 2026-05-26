from sqlalchemy import Column, Integer, String

from database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    nome = Column(String)

    email = Column(String, unique=True)

    senha = Column(String)

    tipo = Column(String)