import io
import json
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import aplicacao
from app.database import Base, obter_sessao

URL_BANCO_TESTE = "sqlite:///./banco_teste.db"
motor_teste = create_engine(URL_BANCO_TESTE, connect_args={"check_same_thread": False})
SessaoTeste = sessionmaker(autocommit=False, autoflush=False, bind=motor_teste)


def sobrescrever_sessao():
    db = SessaoTeste()
    try:
        yield db
    finally:
        db.close()


aplicacao.dependency_overrides[obter_sessao] = sobrescrever_sessao
Base.metadata.create_all(bind=motor_teste)
cliente = TestClient(aplicacao)


@pytest.fixture(autouse=True)
def limpar_banco():
    yield
    Base.metadata.drop_all(bind=motor_teste)
    Base.metadata.create_all(bind=motor_teste)


def _criar_webhook():
    resposta = cliente.post("/api/webhooks/", json={
        "nome": "Webhook Teste",
        "url": "http://localhost:5678/webhook/teste-audio",
    })
    return resposta.json()["id"]


class TestWebhooks:
    def test_criar_webhook_retorna_201(self):
        resposta = cliente.post("/api/webhooks/", json={
            "nome": "Prod",
            "url": "http://n8n/webhook/audio",
        })
        assert resposta.status_code == 201
        assert resposta.json()["nome"] == "Prod"

    def test_listar_webhooks_retorna_200(self):
        _criar_webhook()
        resposta = cliente.get("/api/webhooks/")
        assert resposta.status_code == 200
        assert len(resposta.json()) == 1

    def test_deletar_webhook_retorna_204(self):
        webhook_id = _criar_webhook()
        resposta = cliente.delete(f"/api/webhooks/{webhook_id}")
        assert resposta.status_code == 204

    def test_buscar_webhook_inexistente_retorna_404(self):
        resposta = cliente.get("/api/webhooks/id-inexistente")
        assert resposta.status_code == 404


class TestCasosDeTeste:
    def test_criar_caso_retorna_201(self):
        webhook_id = _criar_webhook()
        audio = io.BytesIO(b"audio-simulado")
        audio.name = "teste.ogg"
        campos = json.dumps([{"chave": "pescador", "valor": "João"}])

        resposta = cliente.post("/api/casos/", data={
            "nome": "Caso 1",
            "webhook_id": webhook_id,
            "campos_esperados": campos,
        }, files={"arquivo_audio": ("teste.ogg", audio, "audio/ogg")})

        assert resposta.status_code == 201
        corpo = resposta.json()
        assert corpo["nome"] == "Caso 1"
        assert len(corpo["campos_esperados"]) == 1

    def test_listar_casos_retorna_200(self):
        resposta = cliente.get("/api/casos/")
        assert resposta.status_code == 200
        assert isinstance(resposta.json(), list)

    def test_deletar_caso_retorna_204(self):
        webhook_id = _criar_webhook()
        audio = io.BytesIO(b"audio")
        campos = json.dumps([])
        resp = cliente.post("/api/casos/", data={
            "nome": "Remover",
            "webhook_id": webhook_id,
            "campos_esperados": campos,
        }, files={"arquivo_audio": ("r.ogg", audio, "audio/ogg")})
        caso_id = resp.json()["id"]
        resposta = cliente.delete(f"/api/casos/{caso_id}")
        assert resposta.status_code == 204
