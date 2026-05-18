from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import obter_sessao
from app.schemas.webhook import WebhookCriar, WebhookAtualizar, WebhookResposta
from app.services import servico_webhook

roteador = APIRouter(prefix="/api/webhooks", tags=["webhooks"])


@roteador.get("/", response_model=list[WebhookResposta])
def listar_webhooks(db: Session = Depends(obter_sessao)):
    return servico_webhook.listar_webhooks(db)


@roteador.post("/", response_model=WebhookResposta, status_code=status.HTTP_201_CREATED)
def criar_webhook(dados: WebhookCriar, db: Session = Depends(obter_sessao)):
    return servico_webhook.criar_webhook(db, dados)


@roteador.get("/{webhook_id}", response_model=WebhookResposta)
def buscar_webhook(webhook_id: str, db: Session = Depends(obter_sessao)):
    return servico_webhook.buscar_webhook(db, webhook_id)


@roteador.put("/{webhook_id}", response_model=WebhookResposta)
def atualizar_webhook(webhook_id: str, dados: WebhookAtualizar, db: Session = Depends(obter_sessao)):
    return servico_webhook.atualizar_webhook(db, webhook_id, dados)


@roteador.delete("/{webhook_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_webhook(webhook_id: str, db: Session = Depends(obter_sessao)):
    servico_webhook.deletar_webhook(db, webhook_id)
