import json
from fastapi import APIRouter, Depends, Form, UploadFile, File, status
from sqlalchemy.orm import Session
from app.database import obter_sessao
from app.schemas.caso_de_teste import CasoCriar, CasoAtualizar, CasoResposta, CampoEsperadoSchema
from app.services import servico_casos

roteador = APIRouter(prefix="/api/casos", tags=["casos-de-teste"])


@roteador.get("/", response_model=list[CasoResposta])
def listar_casos(db: Session = Depends(obter_sessao)):
    return servico_casos.listar_casos(db)


@roteador.post("/", response_model=CasoResposta, status_code=status.HTTP_201_CREATED)
async def criar_caso(
    nome: str = Form(...),
    webhook_id: str = Form(...),
    descricao: str | None = Form(None),
    campos_esperados: str = Form("[]"),
    arquivo_audio: UploadFile = File(...),
    db: Session = Depends(obter_sessao),
):
    campos = [CampoEsperadoSchema(**c) for c in json.loads(campos_esperados)]
    dados = CasoCriar(nome=nome, descricao=descricao, webhook_id=webhook_id, campos_esperados=campos)
    return await servico_casos.criar_caso(db, dados, arquivo_audio)


@roteador.get("/{caso_id}", response_model=CasoResposta)
def buscar_caso(caso_id: str, db: Session = Depends(obter_sessao)):
    caso = servico_casos.buscar_caso(db, caso_id)
    from app.repositories import repositorio_execucoes
    ultima = repositorio_execucoes.ultima_por_caso(db, caso_id)
    resposta = CasoResposta.model_validate(caso)
    resposta.ultimo_status = ultima.status if ultima else None
    return resposta


@roteador.put("/{caso_id}", response_model=CasoResposta)
async def atualizar_caso(
    caso_id: str,
    nome: str | None = Form(None),
    descricao: str | None = Form(None),
    webhook_id: str | None = Form(None),
    campos_esperados: str | None = Form(None),
    arquivo_audio: UploadFile | None = File(None),
    db: Session = Depends(obter_sessao),
):
    campos = None
    if campos_esperados is not None:
        campos = [CampoEsperadoSchema(**c) for c in json.loads(campos_esperados)]
    dados = CasoAtualizar(nome=nome, descricao=descricao, webhook_id=webhook_id, campos_esperados=campos)
    return await servico_casos.atualizar_caso(db, caso_id, dados, arquivo_audio)


@roteador.delete("/{caso_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_caso(caso_id: str, db: Session = Depends(obter_sessao)):
    servico_casos.deletar_caso(db, caso_id)
