from datetime import datetime, timedelta

from jose import jwt

SECRET_KEY = "treina_comigo_secret"

ALGORITHM = "HS256"


def criar_token(data: dict):

    dados = data.copy()

    expiracao = datetime.utcnow() + timedelta(days=1)

    dados.update({
        "exp": expiracao
    })

    token = jwt.encode(
        dados,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token