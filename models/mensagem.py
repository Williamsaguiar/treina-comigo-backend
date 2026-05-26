from sqlalchemy import Column, Integer, String

from database.database import Base


class Mensagem(Base):

    __tablename__ = "mensagens"

    id = Column(Integer, primary_key=True, index=True)

    aluno = Column(String)

    personal = Column(String)

    mensagem = Column(String)