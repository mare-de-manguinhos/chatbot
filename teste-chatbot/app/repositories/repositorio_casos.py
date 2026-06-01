from sqlalchemy.orm import Session, joinedload
from app.models.caso_de_teste import CasoDeTeste


def listar(db: Session) -> list[CasoDeTeste]:
    return (
        db.query(CasoDeTeste)
        .options(joinedload(CasoDeTeste.campos_esperados), joinedload(CasoDeTeste.webhook))
        .order_by(CasoDeTeste.criado_em.desc())
        .all()
    )


def buscar_por_id(db: Session, caso_id: str) -> CasoDeTeste | None:
    return (
        db.query(CasoDeTeste)
        .options(joinedload(CasoDeTeste.campos_esperados), joinedload(CasoDeTeste.webhook))
        .filter(CasoDeTeste.id == caso_id)
        .first()
    )


def criar(db: Session, dados: dict) -> CasoDeTeste:
    caso = CasoDeTeste(**dados)
    db.add(caso)
    db.commit()
    db.refresh(caso)
    return caso


def atualizar(db: Session, caso: CasoDeTeste, dados: dict) -> CasoDeTeste:
    for campo, valor in dados.items():
        setattr(caso, campo, valor)
    db.commit()
    db.refresh(caso)
    return caso


def deletar(db: Session, caso: CasoDeTeste) -> None:
    db.delete(caso)
    db.commit()
