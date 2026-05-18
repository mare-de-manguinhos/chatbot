from datetime import datetime
from pydantic import BaseModel


class WebhookCriar(BaseModel):
    nome: str
    descricao: str | None = None
    url: str


class WebhookAtualizar(BaseModel):
    nome: str | None = None
    descricao: str | None = None
    url: str | None = None


class WebhookResposta(BaseModel):
    id: str
    nome: str
    descricao: str | None
    url: str
    criado_em: datetime

    model_config = {"from_attributes": True}
