from sqlalchemy import Column, Integer, String

from database.database import Base


class Favorito(Base):

    __tablename__ = "favoritos"

    id = Column(Integer, primary_key=True, index=True)

    aluno = Column(String)

    personal = Column(String)

    foto = Column(String)

    especialidade = Column(String)