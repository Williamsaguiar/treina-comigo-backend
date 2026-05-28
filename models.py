from sqlalchemy import Column, Integer, String
from database import Base


class Usuario(Base):

    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)

    nome = Column(String)

    email = Column(String, unique=True)

    senha = Column(String)


class Treino(Base):

    __tablename__ = "treinos"

    id = Column(Integer, primary_key=True, index=True)

    nome = Column(String)

    objetivo = Column(String)

    nivel = Column(String)

    descricao = Column(String)


class Academia(Base):

    __tablename__ = "academias"

    id = Column(Integer, primary_key=True, index=True)

    nome = Column(String)

    bairro = Column(String)

    endereco = Column(String)

    nota = Column(String)

    imagem = Column(String)