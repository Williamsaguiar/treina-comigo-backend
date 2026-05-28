from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

from database.database import SessionLocal, engine, Base
from models import Usuario, Treino, Academia

app = FastAPI()

Base.metadata.create_all(bind=engine)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DATABASE
def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()


# HOME
@app.get("/")

def home():

    return {
        "mensagem": "Treina Comigo API 🚀"
    }


# LOGIN
@app.post("/login")

def login(
    dados: dict,
    db: Session = Depends(get_db)
):

    usuario = db.query(Usuario).filter(
        Usuario.email == dados["email"]
    ).first()

    if not usuario:

        return {
            "erro": "Usuário não encontrado"
        }

    if usuario.senha != dados["senha"]:

        return {
            "erro": "Senha inválida"
        }

    return {
        "mensagem": "Login realizado com sucesso",
        "usuario": usuario.nome
    }


# CRIAR USUARIO
@app.post("/usuarios")

def criar_usuario(
    usuario: dict,
    db: Session = Depends(get_db)
):

    novo_usuario = Usuario(

        nome=usuario["nome"],

        email=usuario["email"],

        senha=usuario["senha"]

    )

    db.add(novo_usuario)

    db.commit()

    db.refresh(novo_usuario)

    return novo_usuario


# LISTAR TREINOS
@app.get("/treinos")

def listar_treinos(
    db: Session = Depends(get_db)
):

    return db.query(Treino).all()


# CRIAR TREINO
@app.post("/treinos")

def criar_treino(
    treino: dict,
    db: Session = Depends(get_db)
):

    novo_treino = Treino(

        nome=treino["nome"],

        objetivo=treino["objetivo"],

        nivel=treino["nivel"],

        descricao=treino["descricao"]

    )

    db.add(novo_treino)

    db.commit()

    db.refresh(novo_treino)

    return novo_treino


# LISTAR ACADEMIAS
@app.get("/academias")

def listar_academias(
    db: Session = Depends(get_db)
):

    return db.query(Academia).all()


# CRIAR ACADEMIA
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

        imagem=academia["imagem"]

    )

    db.add(nova_academia)

    db.commit()

    db.refresh(nova_academia)

    return nova_academia

# AGENDAMENTOS
@app.post("/agendamentos")

def criar_agendamento(
    agendamento: dict
):

    return {

        "mensagem":
        f"Treino '{agendamento['nome']}' agendado para {agendamento['horario']} 🚀"

    }

# PERSONAIS
@app.get("/personais")

def listar_personais():

    return [

        {
            "id": 1,
            "nome": "Carlos Henrique",
            "especialidade": "Hipertrofia",
            "foto": "https://randomuser.me/api/portraits/men/32.jpg"
        },

        {
            "id": 2,
            "nome": "Amanda Silva",
            "especialidade": "Emagrecimento",
            "foto": "https://randomuser.me/api/portraits/women/44.jpg"
        }

    ]