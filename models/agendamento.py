from sqlalchemy import Column, Integer, String

from database.database import Base


class Agendamento(Base):

    __tablename__ = "agendamentos"

    id = Column(Integer, primary_key=True, index=True)

    aluno = Column(String)

    personal = Column(String)

    data = Column(String)

    horario = Column(String)