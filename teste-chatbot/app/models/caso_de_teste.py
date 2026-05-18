import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class CasoDeTeste(Base):
    __tablename__ = "casos_de_teste"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    nome: Mapped[str] = mapped_column(String, nullable=False)
    descricao: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    webhook_id: Mapped[str] = mapped_column(String, ForeignKey("webhooks.id"), nullable=False)
    nome_arquivo_audio: Mapped[str] = mapped_column(String, nullable=False)
    caminho_audio: Mapped[str] = mapped_column(String, nullable=False)
    criado_em: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    webhook: Mapped["Webhook"] = relationship("Webhook", back_populates="casos")
    campos_esperados: Mapped[list["CampoEsperado"]] = relationship(
        "CampoEsperado", back_populates="caso_de_teste", cascade="all, delete-orphan"
    )
    execucoes: Mapped[list["Execucao"]] = relationship(
        "Execucao", back_populates="caso_de_teste", cascade="all, delete-orphan"
    )
