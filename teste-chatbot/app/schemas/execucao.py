from datetime import datetime
from pydantic import BaseModel


class DiferencaCampo(BaseModel):
    chave: str
    esperado: str
    obtido: str | None
    passou: bool


class ResultadoComparacao(BaseModel):
    passou: bool
    total_verificado: int
    falhas: list[DiferencaCampo]


class ExecucaoResposta(BaseModel):
    id: str
    caso_de_teste_id: str
    status: str
    transcricao_obtida: str | None
    json_obtido: str | None
    resultado_comparacao: str | None
    mensagem_erro: str | None
    executado_em: datetime
    duracao_ms: int

    model_config = {"from_attributes": True}


class SumarioExecucoes(BaseModel):
    total: int
    aprovados: int
    reprovados: int
    erros: int
