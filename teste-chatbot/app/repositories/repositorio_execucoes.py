from sqlalchemy.orm import Session
from app.models.execucao import Execucao


def criar(db: Session, dados: dict) -> Execucao:
    execucao = Execucao(**dados)
    db.add(execucao)
    db.commit()
    db.refresh(execucao)
    return execucao


def atualizar(db: Session, execucao: Execucao, dados: dict) -> Execucao:
    for campo, valor in dados.items():
        setattr(execucao, campo, valor)
    db.commit()
    db.refresh(execucao)
    return execucao


def buscar_por_id(db: Session, execucao_id: str) -> Execucao | None:
    return db.query(Execucao).filter(Execucao.id == execucao_id).first()


def listar_por_caso(db: Session, caso_id: str, limite: int = 20) -> list[Execucao]:
    return (
        db.query(Execucao)
        .filter(Execucao.caso_de_teste_id == caso_id)
        .order_by(Execucao.executado_em.desc())
        .limit(limite)
        .all()
    )


def ultima_por_caso(db: Session, caso_id: str) -> Execucao | None:
    return (
        db.query(Execucao)
        .filter(Execucao.caso_de_teste_id == caso_id)
        .order_by(Execucao.executado_em.desc())
        .first()
    )
