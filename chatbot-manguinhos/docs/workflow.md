# Workflow n8n

Detalhes internos do fluxo de processamento de áudio.

## Diagrama

```
Webhook → Filtrar Áudio → Download Áudio → Base64→Binário → Gemini Transcrever → Responder WhatsApp
```

## Nós do Workflow

| # | Nó | Tipo | Função |
|---|----|------|--------|
| 1 | **Webhook Evolution API** | Webhook | Recebe `POST /webhook/evolution` da Evolution API |
| 2 | **Filtrar Mensagens de Áudio** | Code (JS) | Verifica se é `audioMessage`, extrai `messageId` e `remoteJid` |
| 3 | **Verificar Múltiplos Áudios** | If | Rejeita lotes com mais de um áudio simultâneo |
| 4 | **Download Áudio** | HTTP Request | `POST` para Evolution API `getBase64FromMediaMessage` |
| 5 | **Base64 → Binário** | Code (JS) | Converte áudio base64 para binary data `.ogg` |
| 6 | **Gemini - Transcrever Áudio** | Google Gemini | Transcreve o áudio usando `gemini-2.5-flash` |
| 7 | **Responder no WhatsApp** | HTTP Request | `POST` para Evolution API `sendText` com a transcrição |

## Detalhes Técnicos

### Filtro de Mensagens

O nó de filtro aceita apenas `audioMessage` do evento `messages.upsert`. Mensagens de texto, imagem ou outros tipos são descartadas silenciosamente.

### Download do Áudio

A Evolution API retorna o áudio em Base64 via endpoint `getBase64FromMediaMessage`. O Webhook Base64 precisa estar habilitado na instância para que isso funcione.

### Transcrição com Gemini

O modelo `gemini-2.5-flash` é usado pela relação custo-benefício — rápido e gratuito via AI Studio para volumes típicos de uso. O áudio `.ogg` é enviado diretamente ao modelo para transcrição.

### Resposta ao Pescador

A transcrição é enviada de volta ao número de origem via `sendText` da Evolution API, fechando o ciclo do fluxo.

## Credenciais Necessárias no n8n

| Credencial | Usada em | Tipo |
|------------|----------|------|
| Google Gemini API Key | Nó Gemini | `Google Gemini (PaLM) Api` |
| Evolution API Key | Nós de HTTP Request | Header `apikey` |
