import os
import shutil
from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session
from app.models.caso_de_teste import CasoDeTeste
from app.schemas.caso_de_teste import CasoCriar, CasoAtualizar, CasoResposta
from app.repositories import repositorio_casos, repositorio_campos, repositorio_execucoes

PASTA_AUDIO = "audio"


def _garantir_pasta_audio():
    os.makedirs(PASTA_AUDIO, exist_ok=True)


def listar_casos(db: Session) -> list[CasoResposta]:
    casos = repositorio_casos.listar(db)
    resultado = []
    for caso in casos:
        ultima = repositorio_execucoes.ultima_por_caso(db, caso.id)
        resposta = CasoResposta.model_validate(caso)
        resposta.ultimo_status = ultima.status if ultima else None
        resultado.append(resposta)
    return resultado


def buscar_caso(db: Session, caso_id: str) -> CasoDeTeste:
    caso = repositorio_casos.buscar_por_id(db, caso_id)
    if not caso:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Caso de teste não encontrado")
    return caso


async def criar_caso(db: Session, dados: CasoCriar, arquivo_audio: UploadFile) -> CasoDeTeste:
    _garantir_pasta_audio()
    nome_arquivo = arquivo_audio.filename or "audio.ogg"
    caminho = os.path.join(PASTA_AUDIO, nome_arquivo)

    with open(caminho, "wb") as destino:
        shutil.copyfileobj(arquivo_audio.file, destino)

    dados_caso = {
        "nome": dados.nome,
        "descricao": dados.descricao,
        "webhook_id": dados.webhook_id,
        "nome_arquivo_audio": nome_arquivo,
        "caminho_audio": os.path.abspath(caminho),
    }
    caso = repositorio_casos.criar(db, dados_caso)

    if dados.campos_esperados:
        repositorio_campos.criar_varios(
            db, caso.id, [c.model_dump() for c in dados.campos_esperados]
        )

    return repositorio_casos.buscar_por_id(db, caso.id)


async def atualizar_caso(
    db: Session, caso_id: str, dados: CasoAtualizar, arquivo_audio: UploadFile | None = None
) -> CasoDeTeste:
    caso = buscar_caso(db, caso_id)

    campos_para_atualizar = {k: v for k, v in dados.model_dump().items() if v is not None and k != "campos_esperados"}

    if arquivo_audio:
        _garantir_pasta_audio()
        nome_arquivo = arquivo_audio.filename or "audio.ogg"
        caminho = os.path.join(PASTA_AUDIO, nome_arquivo)
        with open(caminho, "wb") as destino:
            shutil.copyfileobj(arquivo_audio.file, destino)
        campos_para_atualizar["nome_arquivo_audio"] = nome_arquivo
        campos_para_atualizar["caminho_audio"] = os.path.abspath(caminho)

    if campos_para_atualizar:
        repositorio_casos.atualizar(db, caso, campos_para_atualizar)

    if dados.campos_esperados is not None:
        repositorio_campos.deletar_por_caso(db, caso_id)
        repositorio_campos.criar_varios(
            db, caso_id, [c.model_dump() for c in dados.campos_esperados]
        )

    return repositorio_casos.buscar_por_id(db, caso_id)


def deletar_caso(db: Session, caso_id: str) -> None:
    caso = buscar_caso(db, caso_id)
    if os.path.exists(caso.caminho_audio):
        os.remove(caso.caminho_audio)
    repositorio_casos.deletar(db, caso)
