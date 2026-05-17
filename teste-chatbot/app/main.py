import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.database import motor, Base
from app.models import Webhook, CasoDeTeste, CampoEsperado, Execucao  # noqa: F401 — registra models
from app.controllers import webhooks, casos_de_teste, execucoes


@asynccontextmanager
async def ciclo_de_vida(app: FastAPI):
    Base.metadata.create_all(bind=motor)
    yield


app = FastAPI(
    title="teste-chatbot",
    description="Sistema de testes para o agente n8n de transcrição de áudio",
    version="1.0.0",
    lifespan=ciclo_de_vida,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(webhooks.roteador)
app.include_router(casos_de_teste.roteador)
app.include_router(execucoes.roteador)

# Serve o frontend React em produção (após npm run build)
pasta_dist = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
if os.path.exists(pasta_dist):
    app.mount("/", StaticFiles(directory=pasta_dist, html=True), name="frontend")
