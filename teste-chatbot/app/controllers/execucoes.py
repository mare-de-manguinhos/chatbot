from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import obter_sessao
from app.schemas.execucao import ExecucaoResposta, SumarioExecucoes
from app.services import servico_execucao

roteador = APIRouter(tags=["execucoes"])


@roteador.post("/api/casos/{caso_id}/executar", response_model=ExecucaoResposta, status_code=status.HTTP_201_CREATED)
async def executar_caso(caso_id: str, db: Session = Depends(obter_sessao)):
    return await servico_execucao.executar_caso(db, caso_id)


@roteador.get("/api/casos/{caso_id}/execucoes", response_model=list[ExecucaoResposta])
def listar_execucoes(caso_id: str, db: Session = Depends(obter_sessao)):
    return servico_execucao.listar_execucoes_do_caso(db, caso_id)


@roteador.post("/api/execucoes/executar-todos", response_model=SumarioExecucoes)
async def executar_todos(db: Session = Depends(obter_sessao)):
    return await servico_execucao.executar_todos(db)


@roteador.get("/api/execucoes/{execucao_id}", response_model=ExecucaoResposta)
def buscar_execucao(execucao_id: str, db: Session = Depends(obter_sessao)):
    return servico_execucao.buscar_execucao(db, execucao_id)
