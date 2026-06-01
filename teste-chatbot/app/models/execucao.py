import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, Integer, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Execucao(Base):
    __tablename__ = "execucoes"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    caso_de_teste_id: Mapped[str] = mapped_column(String, ForeignKey("casos_de_teste.id"), nullable=False)
    # 'pendente' | 'executando' | 'aprovado' | 'reprovado' | 'erro'
    status: Mapped[str] = mapped_column(String, nullable=False, default="pendente")
    transcricao_obtida: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    json_obtido: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    resultado_comparacao: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    mensagem_erro: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    executado_em: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    duracao_ms: Mapped[int] = mapped_column(Integer, default=0)

    caso_de_teste: Mapped["CasoDeTeste"] = relationship("CasoDeTeste", back_populates="execucoes")
