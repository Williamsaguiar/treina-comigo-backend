from sqlalchemy import Column, Integer, String

from database.database import Base


class Avaliacao(Base):

    __tablename__ = "avaliacoes"

    id = Column(Integer, primary_key=True, index=True)

    aluno = Column(String)

    personal = Column(String)

    nota = Column(Integer)

    comentario = Column(String)