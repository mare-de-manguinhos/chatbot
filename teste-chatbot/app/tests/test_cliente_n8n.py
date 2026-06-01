import base64
import os
import tempfile
import pytest
import httpx
from unittest.mock import AsyncMock, patch, MagicMock
from app.services.cliente_n8n import enviar_audio, ErroConexaoN8N, ErroTimeoutN8N


@pytest.fixture
def arquivo_audio_temporario():
    with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as f:
        f.write(b"audio-simulado")
        caminho = f.name
    yield caminho
    os.unlink(caminho)


class TestEnviarAudio:
    @pytest.mark.asyncio
    async def test_envio_bem_sucedido_retorna_json(self, arquivo_audio_temporario):
        resposta_simulada = MagicMock()
        resposta_simulada.json.return_value = {"pescador": "João", "transcricao": "teste"}
        resposta_simulada.raise_for_status = MagicMock()

        with patch("httpx.AsyncClient") as mock_cliente:
            mock_cliente.return_value.__aenter__.return_value.post = AsyncMock(return_value=resposta_simulada)
            resultado = await enviar_audio("http://n8n/webhook/teste", arquivo_audio_temporario, "audio.ogg")

        assert resultado["pescador"] == "João"
        assert resultado["transcricao"] == "teste"

    @pytest.mark.asyncio
    async def test_timeout_lanca_erro_timeout(self, arquivo_audio_temporario):
        with patch("httpx.AsyncClient") as mock_cliente:
            mock_cliente.return_value.__aenter__.return_value.post = AsyncMock(
                side_effect=httpx.TimeoutException("timeout")
            )
            with pytest.raises(ErroTimeoutN8N):
                await enviar_audio("http://n8n/webhook/teste", arquivo_audio_temporario, "audio.ogg")

    @pytest.mark.asyncio
    async def test_conexao_recusada_lanca_erro_conexao(self, arquivo_audio_temporario):
        with patch("httpx.AsyncClient") as mock_cliente:
            mock_cliente.return_value.__aenter__.return_value.post = AsyncMock(
                side_effect=httpx.ConnectError("recusado")
            )
            with pytest.raises(ErroConexaoN8N):
                await enviar_audio("http://n8n/webhook/teste", arquivo_audio_temporario, "audio.ogg")

    @pytest.mark.asyncio
    async def test_status_erro_http_lanca_erro_conexao(self, arquivo_audio_temporario):
        resposta_simulada = MagicMock()
        resposta_simulada.status_code = 500
        resposta_simulada.text = "erro interno"
        resposta_simulada.raise_for_status.side_effect = httpx.HTTPStatusError(
            "500", request=MagicMock(), response=resposta_simulada
        )

        with patch("httpx.AsyncClient") as mock_cliente:
            mock_cliente.return_value.__aenter__.return_value.post = AsyncMock(return_value=resposta_simulada)
            with pytest.raises(ErroConexaoN8N):
                await enviar_audio("http://n8n/webhook/teste", arquivo_audio_temporario, "audio.ogg")
