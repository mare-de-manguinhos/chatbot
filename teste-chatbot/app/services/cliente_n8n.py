import base64
import httpx


class ErroConexaoN8N(Exception):
    pass


class ErroTimeoutN8N(Exception):
    pass


async def enviar_audio(url_webhook: str, caminho_audio: str, nome_arquivo: str) -> dict:
    with open(caminho_audio, "rb") as arquivo:
        audio_base64 = base64.b64encode(arquivo.read()).decode("utf-8")

    payload = {
        "audio_base64": audio_base64,
        "nome_arquivo": nome_arquivo,
    }

    try:
        async with httpx.AsyncClient(timeout=60.0) as cliente:
            resposta = await cliente.post(url_webhook, json=payload)
            resposta.raise_for_status()
            return resposta.json()
    except httpx.TimeoutException as erro:
        raise ErroTimeoutN8N(f"Timeout ao chamar o webhook n8n: {url_webhook}") from erro
    except httpx.ConnectError as erro:
        raise ErroConexaoN8N(f"Não foi possível conectar ao webhook n8n: {url_webhook}") from erro
    except httpx.HTTPStatusError as erro:
        raise ErroConexaoN8N(
            f"Webhook n8n retornou erro {erro.response.status_code}: {erro.response.text}"
        ) from erro
