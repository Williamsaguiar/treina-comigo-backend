from models.favorito import Favorito
from models.avaliacao import Avaliacao
from models.mensagem import Mensagem
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session
from fastapi import Depends
from database.database import SessionLocal

from models.agendamento import Agendamento
from models.personal import Personal
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.database import engine, SessionLocal
from models.user import User

from auth.security import criar_token

app = FastAPI()

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

from database.database import Base

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "API Treina Comigo Online 🚀"
    }


@app.get("/academias")
def academias():

    return [

        {
            "id": 1,
            "nome": "IronFit Academia",
            "imagem": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?q=80&w=1200",
            "avaliacao": 4.8,
            "distancia": "350m",
            "diaria": 25
        },

        {
            "id": 2,
            "nome": "Blue Gym",
            "imagem": "https://images.unsplash.com/photo-1571902943202-507ec2618e8f?q=80&w=1200",
            "avaliacao": 4.7,
            "distancia": "500m",
            "diaria": 20
        }
    ]


@app.post("/cadastro")
def cadastro(usuario: dict):

    db = SessionLocal()

    novo_usuario = User(
        nome=usuario["nome"],
        email=usuario["email"],
        senha=usuario["senha"],
        tipo=usuario["tipo"]
    )

    db.add(novo_usuario)

    db.commit()

    db.refresh(novo_usuario)

    return {
        "message": "Usuário cadastrado com sucesso 🚀"
    }


@app.post("/login")
def login(usuario: dict):

    db = SessionLocal()

    usuario_db = db.query(User).filter(
        User.email == usuario["email"]
    ).first()

    if not usuario_db:
        return {
            "error": "Usuário não encontrado"
        }

    if usuario_db.senha != usuario["senha"]:
        return {
            "error": "Senha inválida"
        }

    token = criar_token({
        "id": usuario_db.id,
        "email": usuario_db.email
    })

    return {
        "token": token,
        "usuario": {
            "id": usuario_db.id,
            "nome": usuario_db.nome,
            "tipo": usuario_db.tipo
        }
    }

@app.get("/personais")
def listar_personais():

    return [

        {
            "id": 1,
            "nome": "Carlos Personal",
            "foto": "https://images.unsplash.com/photo-1567013127542-490d757e51fc?q=80&w=1200",
            "especialidade": "Hipertrofia",
            "descricao": "Treinos para ganho de massa muscular",
            "valor_hora": 80
        },

        {
            "id": 2,
            "nome": "Ana Fitness",
            "foto": "https://images.unsplash.com/photo-1594737625785-a6cbdabd333c?q=80&w=1200",
            "especialidade": "Emagrecimento",
            "descricao": "Treinos para perda de gordura",
            "valor_hora": 70
        }
    ]

@app.post("/agendamentos")
def criar_agendamento(
    dados: dict,
    db: Session = Depends(get_db)
):

    agendamento_existente = db.query(
        Agendamento
    ).filter(

        Agendamento.personal == dados["personal"],

        Agendamento.data == dados["data"],

        Agendamento.horario == dados["horario"]

    ).first()

    if agendamento_existente:

        return {
            "error": "Horário já agendado"
        }

    novo_agendamento = Agendamento(

        aluno=dados["aluno"],

        personal=dados["personal"],

        data=dados["data"],

        horario=dados["horario"],
    )

    db.add(novo_agendamento)

    db.commit()

    db.refresh(novo_agendamento)

    return {
        "message": "Treino agendado com sucesso 🚀"
    }

@app.get("/agendamentos")
def listar_agendamentos(
    db: Session = Depends(get_db)
):

    agendamentos = db.query(
        Agendamento
    ).all()

    return agendamentos

@app.delete("/agendamentos/{agendamento_id}")
def deletar_agendamento(
    agendamento_id: int,
    db: Session = Depends(get_db)
):

    agendamento = db.query(
        Agendamento
    ).filter(
        Agendamento.id == agendamento_id
    ).first()

    if not agendamento:

        return {
            "error": "Agendamento não encontrado"
        }

    db.delete(agendamento)

    db.commit()

    return {
        "message": "Agendamento cancelado 🚀"
    }

@app.get("/agendamentos/personal/{nome}/{data}")
def listar_agendamentos_personal(
    nome: str,
    data: str,
    db: Session = Depends(get_db)
):

    agendamentos = db.query(
        Agendamento
    ).filter(

        Agendamento.personal == nome,

        Agendamento.data == data

    ).all()

    return agendamentos

@app.post("/favoritos")
def criar_favorito(
    dados: dict,
    db: Session = Depends(get_db)
):

    favorito_existente = db.query(
        Favorito
    ).filter(

        Favorito.aluno == dados["aluno"],

        Favorito.personal == dados["personal"]

    ).first()

    if favorito_existente:

        return {
            "error": "Personal já favoritado"
        }

    novo_favorito = Favorito(

        aluno=dados["aluno"],

        personal=dados["personal"],

        foto=dados["foto"],

        especialidade=dados["especialidade"],
    )

    db.add(novo_favorito)

    db.commit()

    db.refresh(novo_favorito)

    return {
        "message": "Favoritado com sucesso ❤️"
    }


@app.get("/favoritos")
def listar_favoritos(
    db: Session = Depends(get_db)
):

    favoritos = db.query(
        Favorito
    ).all()

    return favoritos

@app.post("/avaliacoes")
def criar_avaliacao(
    dados: dict,
    db: Session = Depends(get_db)
):

    nova_avaliacao = Avaliacao(

        aluno=dados["aluno"],

        personal=dados["personal"],

        nota=dados["nota"],

        comentario=dados["comentario"],
    )

    db.add(nova_avaliacao)

    db.commit()

    db.refresh(nova_avaliacao)

    return {
        "message": "Avaliação enviada ⭐"
    }


@app.get("/avaliacoes/{personal}")
def listar_avaliacoes(
    personal: str,
    db: Session = Depends(get_db)
):

    avaliacoes = db.query(
        Avaliacao
    ).filter(
        Avaliacao.personal == personal
    ).all()

    return avaliacoes

@app.post("/mensagens")
def enviar_mensagem(
    dados: dict,
    db: Session = Depends(get_db)
):

    nova_mensagem = Mensagem(

        aluno=dados["aluno"],

        personal=dados["personal"],

        mensagem=dados["mensagem"],
    )

    db.add(nova_mensagem)

    db.commit()

    db.refresh(nova_mensagem)

    return {
        "message": "Mensagem enviada 🚀"
    }


@app.get("/mensagens/{personal}")
def listar_mensagens(
    personal: str,
    db: Session = Depends(get_db)
):

    mensagens = db.query(
        Mensagem
    ).filter(
        Mensagem.personal == personal
    ).all()

    return mensagens