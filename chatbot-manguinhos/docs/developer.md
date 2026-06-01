# Para Desenvolvedores

Guia para subir o ambiente completo localmente.

## Pré-requisitos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado e rodando
- API Key do Google AI Studio — gratuita, obter em [aistudio.google.com](https://aistudio.google.com/)
- Git

## 1. Clonar o repositório

```bash
git clone <url-do-repositorio>
cd chatbot
```

## 2. Subir os containers

```bash
docker compose up -d
```

Aguarde todos os serviços ficarem saudáveis. PostgreSQL e Redis possuem healthchecks:

```bash
docker compose ps
```

A primeira execução pode demorar alguns minutos para baixar as imagens (~500 MB).

## 3. Configurar a Evolution API

### 3.1 — Acessar o Gerenciador

Abra no navegador: **http://localhost:8080/manager**

Credenciais padrão:

- **API Key**: `sua_chave_api_super_secreta`

### 3.2 — Criar instância e conectar WhatsApp

1. Clique em **"Create Instance"**
2. Escolha um nome (ex: `pescadores`)
3. **Integration**: `WHATSAPP-BAILEYS`
4. Clique em **"Connect"** para gerar o QR Code
5. Escaneie com o celular:
   - **WhatsApp → Configurações → Dispositivos Vinculados → Vincular Dispositivo**

!!! tip "QR Code não aparece?"
    Verifique os logs: `docker compose logs -f evolution-api`

    A variável `CONFIG_SESSION_PHONE_VERSION` no `docker-compose.yml` pode estar desatualizada — pegue a versão atual em [wppconnect.io/whatsapp-versions](https://wppconnect.io/whatsapp-versions/).

### 3.3 — Configurar Webhook

No painel da Evolution API, vá em **Events → Webhook** e preencha:

| Campo | Valor |
|-------|-------|
| **Enabled** | ✅ ligado |
| **URL** | `http://bot-n8n:5678/webhook/evolution` |
| **Webhook Base64** | ✅ ligado |
| **Events** | `MESSAGES_UPSERT` (mínimo) |

!!! warning "Atenção"
    A URL usa `bot-n8n` (nome do container na rede Docker interna), **não** `localhost`.

## 4. Configurar o n8n

### 4.1 — Acessar o n8n

Abra no navegador: **http://localhost:5678**

Na primeira vez, crie uma conta (dados ficam salvos localmente no volume Docker).

### 4.2 — Adicionar credencial do Google Gemini

1. **Settings → Credentials → Add Credential**
2. Busque `Google Gemini (PaLM) Api`
3. Cole sua API Key do Google AI Studio
4. Salve

### 4.3 — Importar o Workflow

1. **Add Workflow → Import from File**
2. Selecione `chat-bot-workflow.json` da raiz do repositório
3. No nó **"Gemini - Transcrever Áudio"**, selecione a credencial criada acima
4. Nos nós **"Download Áudio"** e **"Responder no WhatsApp"**, confirme que os headers têm `apikey: sua_chave_api_super_secreta`
5. Clique em **"Save"** e ative o workflow (toggle no canto superior direito)

## 5. Testar

1. De outro celular, envie um **áudio** via WhatsApp para o número conectado
2. O bot deve responder com a transcrição em poucos segundos
3. Acompanhe a execução em **Executions** no menu lateral do n8n

## Variáveis de Ambiente

As variáveis com padrão podem ser sobrescritas criando um arquivo `.env` na raiz:

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| `POSTGRES_USER` | `bot_user` | Usuário do banco |
| `POSTGRES_PASSWORD` | `bot_password` | Senha do banco |
| `POSTGRES_DB` | `bot_db` | Nome do banco |
| `N8N_USER` | `admin` | Usuário do n8n |
| `N8N_PASSWORD` | `senha_ifes` | Senha do n8n |
| `EVOLUTION_API_KEY` | `sua_chave_api_super_secreta` | Chave de autenticação da Evolution API |
| `EVOLUTION_SERVER_URL` | `http://localhost:8080` | URL pública da Evolution API |
| `N8N_WEBHOOK_URL` | `http://localhost:5678/` | URL base do n8n para webhooks |

## Comandos Úteis

```bash
# Ver status dos containers
docker compose ps

# Ver logs de um serviço específico
docker compose logs -f evolution-api
docker compose logs -f n8n

# Reiniciar todos os serviços
docker compose down && docker compose up -d

# Reiniciar apenas um serviço
docker compose restart n8n
```
