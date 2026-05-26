from sqlalchemy import Column, Integer, String, Float

from database.database import Base


class Personal(Base):

    __tablename__ = "personais"

    id = Column(Integer, primary_key=True, index=True)

    nome = Column(String)

    foto = Column(String)

    especialidade = Column(String)

    descricao = Column(String)

    valor_hora = Column(Float)