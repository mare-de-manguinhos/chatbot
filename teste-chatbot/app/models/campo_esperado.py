import uuid
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class CampoEsperado(Base):
    __tablename__ = "campos_esperados"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    caso_de_teste_id: Mapped[str] = mapped_column(String, ForeignKey("casos_de_teste.id"), nullable=False)
    chave: Mapped[str] = mapped_column(String, nullable=False)
    valor: Mapped[str] = mapped_column(String, nullable=False)

    caso_de_teste: Mapped["CasoDeTeste"] = relationship("CasoDeTeste", back_populates="campos_esperados")
