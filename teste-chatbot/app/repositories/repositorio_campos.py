from sqlalchemy.orm import Session
from app.models.campo_esperado import CampoEsperado


def listar_por_caso(db: Session, caso_id: str) -> list[CampoEsperado]:
    return db.query(CampoEsperado).filter(CampoEsperado.caso_de_teste_id == caso_id).all()


def criar_varios(db: Session, caso_id: str, campos: list[dict]) -> list[CampoEsperado]:
    novos = [CampoEsperado(caso_de_teste_id=caso_id, **c) for c in campos]
    db.add_all(novos)
    db.commit()
    return novos


def deletar_por_caso(db: Session, caso_id: str) -> None:
    db.query(CampoEsperado).filter(CampoEsperado.caso_de_teste_id == caso_id).delete()
    db.commit()
