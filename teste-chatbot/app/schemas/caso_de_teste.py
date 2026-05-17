from datetime import datetime
from pydantic import BaseModel


class CampoEsperadoSchema(BaseModel):
    chave: str
    valor: str

    model_config = {"from_attributes": True}


class CasoCriar(BaseModel):
    nome: str
    descricao: str | None = None
    webhook_id: str
    campos_esperados: list[CampoEsperadoSchema] = []


class CasoAtualizar(BaseModel):
    nome: str | None = None
    descricao: str | None = None
    webhook_id: str | None = None
    campos_esperados: list[CampoEsperadoSchema] | None = None


class CasoResposta(BaseModel):
    id: str
    nome: str
    descricao: str | None
    webhook_id: str
    nome_arquivo_audio: str
    criado_em: datetime
    campos_esperados: list[CampoEsperadoSchema]
    ultimo_status: str | None = None

    model_config = {"from_attributes": True}
