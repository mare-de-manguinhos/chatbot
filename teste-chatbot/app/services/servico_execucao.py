import json
import time
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.execucao import Execucao
from app.schemas.execucao import ExecucaoResposta, SumarioExecucoes
from app.repositories import repositorio_execucoes, repositorio_casos, repositorio_webhooks
from app.services import cliente_n8n, comparador


async def executar_caso(db: Session, caso_id: str) -> ExecucaoResposta:
    caso = repositorio_casos.buscar_por_id(db, caso_id)
    if not caso:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Caso de teste não encontrado")

    webhook = repositorio_webhooks.buscar_por_id(db, caso.webhook_id)
    if not webhook:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Webhook associado não encontrado")

    execucao = repositorio_execucoes.criar(db, {
        "caso_de_teste_id": caso_id,
        "status": "executando",
    })

    inicio = time.time()
    try:
        json_obtido = await cliente_n8n.enviar_audio(
            webhook.url, caso.caminho_audio, caso.nome_arquivo_audio
        )
        duracao_ms = int((time.time() - inicio) * 1000)

        resultado = comparador.comparar(caso.campos_esperados, json_obtido)
        status_final = "aprovado" if resultado.passou else "reprovado"
        transcricao = json_obtido.get("transcricao")

        execucao = repositorio_execucoes.atualizar(db, execucao, {
            "status": status_final,
            "transcricao_obtida": transcricao,
            "json_obtido": json.dumps(json_obtido, ensure_ascii=False),
            "resultado_comparacao": resultado.model_dump_json(),
            "duracao_ms": duracao_ms,
        })

    except (cliente_n8n.ErroConexaoN8N, cliente_n8n.ErroTimeoutN8N) as erro:
        duracao_ms = int((time.time() - inicio) * 1000)
        execucao = repositorio_execucoes.atualizar(db, execucao, {
            "status": "erro",
            "mensagem_erro": str(erro),
            "duracao_ms": duracao_ms,
        })

    return ExecucaoResposta.model_validate(execucao)


async def executar_todos(db: Session) -> SumarioExecucoes:
    casos = repositorio_casos.listar(db)
    aprovados = reprovados = erros = 0

    for caso in casos:
        resultado = await executar_caso(db, caso.id)
        if resultado.status == "aprovado":
            aprovados += 1
        elif resultado.status == "reprovado":
            reprovados += 1
        else:
            erros += 1

    return SumarioExecucoes(
        total=len(casos),
        aprovados=aprovados,
        reprovados=reprovados,
        erros=erros,
    )


def buscar_execucao(db: Session, execucao_id: str) -> Execucao:
    execucao = repositorio_execucoes.buscar_por_id(db, execucao_id)
    if not execucao:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Execução não encontrada")
    return execucao


def listar_execucoes_do_caso(db: Session, caso_id: str) -> list[Execucao]:
    return repositorio_execucoes.listar_por_caso(db, caso_id)
