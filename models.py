class Academia(Base):

    __tablename__ = "academias"

    id = Column(Integer, primary_key=True, index=True)

    nome = Column(String)

    bairro = Column(String)

    endereco = Column(String)

    nota = Column(String)

    imagem = Column(String)