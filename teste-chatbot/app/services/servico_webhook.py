from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.webhook import Webhook
from app.schemas.webhook import WebhookCriar, WebhookAtualizar
from app.repositories import repositorio_webhooks


def listar_webhooks(db: Session) -> list[Webhook]:
    return repositorio_webhooks.listar(db)


def buscar_webhook(db: Session, webhook_id: str) -> Webhook:
    webhook = repositorio_webhooks.buscar_por_id(db, webhook_id)
    if not webhook:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Webhook não encontrado")
    return webhook


def criar_webhook(db: Session, dados: WebhookCriar) -> Webhook:
    return repositorio_webhooks.criar(db, dados.model_dump())


def atualizar_webhook(db: Session, webhook_id: str, dados: WebhookAtualizar) -> Webhook:
    webhook = buscar_webhook(db, webhook_id)
    campos_para_atualizar = {k: v for k, v in dados.model_dump().items() if v is not None}
    return repositorio_webhooks.atualizar(db, webhook, campos_para_atualizar)


def deletar_webhook(db: Session, webhook_id: str) -> None:
    webhook = buscar_webhook(db, webhook_id)
    repositorio_webhooks.deletar(db, webhook)
