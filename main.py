from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Academia

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
)

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker

# =========================
# DATABASE
# =========================

DATABASE_URL = "postgresql://neondb_owner:npg_Rpvj3k1LCFDu@ep-wispy-meadow-ac191iug-pooler.sa-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

engine = create_engine(
    DATABASE_URL
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# =========================
# APP
# =========================

app = FastAPI()

# =========================
# CORS
# =========================

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)

# =========================
# MODELOS
# =========================

class Usuario(Base):

    __tablename__ = "usuarios"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    nome = Column(String)

    email = Column(
        String,
        unique=True
    )

    senha = Column(String)


class Agendamento(Base):

    __tablename__ = "agendamentos"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    nome = Column(String)

    horario = Column(String)


class Favorito(Base):

    __tablename__ = "favoritos"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    nome = Column(String)


class Avaliacao(Base):

    __tablename__ = "avaliacoes"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    nome = Column(String)

    comentario = Column(String)

    nota = Column(Integer)


class Mensagem(Base):

    __tablename__ = "mensagens"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    remetente = Column(String)

    destinatario = Column(String)

    mensagem = Column(String)


# =========================
# NOVO MODELO TREINOS
# =========================

class Treino(Base):

    __tablename__ = "treinos"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    nome = Column(String)

    objetivo = Column(String)

    nivel = Column(String)

    descricao = Column(String)

# =========================
# CRIAR TABELAS
# =========================

Base.metadata.create_all(
    bind=engine
)

# =========================
# ROTAS
# =========================

@app.get("/academias")

def listar_academias(db: Session = Depends(get_db)):

    academias =
        db.query(Academia).all()

    return academias

@app.get("/")

def home():

    return {
        "mensagem":
        "API ONLINE 🚀"
    }

# =========================
# USUÁRIOS
# =========================

@app.post("/academias")

def criar_academia(
    academia: dict,
    db: Session = Depends(get_db)
):

    nova_academia = Academia(

        nome=academia["nome"],

        bairro=academia["bairro"],

        endereco=academia["endereco"],

        nota=academia["nota"],

        imagem=academia["imagem"],

    )

    db.add(nova_academia)

    db.commit()

    db.refresh(nova_academia)

    return nova_academia

@app.post("/cadastro")

def cadastro(

    nome: str,

    email: str,

    senha: str,
):

    db = SessionLocal()

    usuario = Usuario(

        nome=nome,

        email=email,

        senha=senha,
    )

    db.add(usuario)

    db.commit()

    return {
        "mensagem":
        "Usuário cadastrado"
    }


@app.post("/login")

def login(

    email: str,

    senha: str,
):

    db = SessionLocal()

    usuario = db.query(
        Usuario
    ).filter(

        Usuario.email == email,

        Usuario.senha == senha

    ).first()

    if usuario:

        return {
            "mensagem":
            "Login realizado"
        }

    return {
        "erro":
        "Usuário inválido"
    }


@app.get("/usuarios")

def listar_usuarios():

    db = SessionLocal()

    usuarios = db.query(
        Usuario
    ).all()

    return usuarios

# =========================
# AGENDAMENTOS
# =========================

@app.post("/agendamentos")

def criar_agendamento(

    nome: str,

    horario: str,
):

    db = SessionLocal()

    agendamento = Agendamento(

        nome=nome,

        horario=horario,
    )

    db.add(agendamento)

    db.commit()

    return {
        "mensagem":
        "Treino agendado"
    }


@app.get("/agendamentos")

def listar_agendamentos():

    db = SessionLocal()

    agendamentos = db.query(
        Agendamento
    ).all()

    return agendamentos

# =========================
# FAVORITOS
# =========================

@app.post("/favoritos")

def adicionar_favorito(

    nome: str,
):

    db = SessionLocal()

    favorito = Favorito(
        nome=nome
    )

    db.add(favorito)

    db.commit()

    return {
        "mensagem":
        "Favorito adicionado"
    }


@app.get("/favoritos")

def listar_favoritos():

    db = SessionLocal()

    favoritos = db.query(
        Favorito
    ).all()

    return favoritos

# =========================
# AVALIAÇÕES
# =========================

@app.post("/avaliacoes")

def criar_avaliacao(

    nome: str,

    comentario: str,

    nota: int,
):

    db = SessionLocal()

    avaliacao = Avaliacao(

        nome=nome,

        comentario=comentario,

        nota=nota,
    )

    db.add(avaliacao)

    db.commit()

    return {
        "mensagem":
        "Avaliação criada"
    }


@app.get("/avaliacoes/{nome}")

def listar_avaliacoes(
    nome: str
):

    db = SessionLocal()

    avaliacoes = db.query(
        Avaliacao
    ).filter(

        Avaliacao.nome == nome

    ).all()

    return avaliacoes

# =========================
# MENSAGENS
# =========================

@app.post("/mensagens")

def enviar_mensagem(

    remetente: str,

    destinatario: str,

    mensagem: str,
):

    db = SessionLocal()

    nova_mensagem = Mensagem(

        remetente=remetente,

        destinatario=destinatario,

        mensagem=mensagem,
    )

    db.add(nova_mensagem)

    db.commit()

    return {
        "mensagem":
        "Mensagem enviada"
    }


@app.get("/mensagens/{destinatario}")

def listar_mensagens(
    destinatario: str
):

    db = SessionLocal()

    mensagens = db.query(
        Mensagem
    ).filter(

        Mensagem.destinatario
        == destinatario

    ).all()

    return mensagens

# =========================
# TREINOS
# =========================

@app.post("/treinos")

def criar_treino(

    nome: str,

    objetivo: str,

    nivel: str,

    descricao: str,
):

    db = SessionLocal()

    treino = Treino(

        nome=nome,

        objetivo=objetivo,

        nivel=nivel,

        descricao=descricao,
    )

    db.add(treino)

    db.commit()

    return {
        "mensagem":
        "Treino criado"
    }


@app.get("/treinos")

def listar_treinos():

    db = SessionLocal()

    treinos = db.query(
        Treino
    ).all()

    return treinos