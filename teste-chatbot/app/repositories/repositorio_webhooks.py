from sqlalchemy.orm import Session
from app.models.webhook import Webhook


def listar(db: Session) -> list[Webhook]:
    return db.query(Webhook).order_by(Webhook.criado_em.desc()).all()


def buscar_por_id(db: Session, webhook_id: str) -> Webhook | None:
    return db.query(Webhook).filter(Webhook.id == webhook_id).first()


def criar(db: Session, dados: dict) -> Webhook:
    webhook = Webhook(**dados)
    db.add(webhook)
    db.commit()
    db.refresh(webhook)
    return webhook


def atualizar(db: Session, webhook: Webhook, dados: dict) -> Webhook:
    for campo, valor in dados.items():
        setattr(webhook, campo, valor)
    db.commit()
    db.refresh(webhook)
    return webhook


def deletar(db: Session, webhook: Webhook) -> None:
    db.delete(webhook)
    db.commit()
