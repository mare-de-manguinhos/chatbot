# 🎣 Bot Pescadores Manguinhos — Transcrição de Áudio via WhatsApp

Bot que recebe áudios de pescadores via WhatsApp, transcreve automaticamente usando **Google Gemini**, e responde com o texto transcrito. Orquestrado por **n8n** (low-code) e conectado ao WhatsApp pela **Evolution API**.

## 🏗️ Arquitetura

```
Pescador (WhatsApp) → Evolution API → n8n Webhook → Gemini (Transcrição) → Resposta WhatsApp
```

**Stack:**

| Serviço | Descrição | Porta |
|---------|-----------|-------|
| **Evolution API** v2.3.7 | Conexão com WhatsApp Web (via Baileys) | `8080` |
| **n8n** | Orquestrador de workflow visual | `5678` |
| **Google Gemini** | Transcrição de áudio (gratuito via AI Studio) | — |
| **PostgreSQL** 15 | Banco de dados para n8n e Evolution | `5432` |
| **Redis** 7 | Cache de sessões WhatsApp | — |

---

## 🚀 Como Rodar

### Pré-requisitos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado e rodando
- API Key do Google AI Studio — gratuita, obter em [aistudio.google.com](https://aistudio.google.com/)

### 1. Subir os containers

```bash
docker compose up -d
```

Aguarde todos os serviços ficarem saudáveis (PostgreSQL e Redis têm healthchecks):

```bash
docker compose ps
```

> **Primeira execução** pode demorar alguns minutos para baixar as imagens Docker (~500MB).

### 2. Configurar a Evolution API

#### 2.1 — Acessar o Gerenciador

Abra no navegador: **http://localhost:8080/manager**

- API Key: `sua_chave_api_super_secreta`

#### 2.2 — Criar Instância e Conectar WhatsApp

1. Clique em **"Create Instance"**
2. Nome da instância: qualquer nome (ex: `pescadores`)
3. Integration: **WHATSAPP-BAILEYS**
4. Clique em **"Connect"** para gerar o QR Code
5. Escaneie com o WhatsApp no celular:
   - **WhatsApp → Configurações → Dispositivos Vinculados → Vincular Dispositivo**

> **QR Code não aparece?** Verifique os logs: `docker compose logs -f evolution-api`. A variável `CONFIG_SESSION_PHONE_VERSION` no `docker-compose.yml` pode precisar ser atualizada — pegue a versão atual em [wppconnect.io/whatsapp-versions](https://wppconnect.io/whatsapp-versions/).

#### 2.3 — Configurar Webhook

Na interface da Evolution API (`http://localhost:8080/manager`), vá em **Events → Webhook** e configure:

- **Enabled**: ✅ ligado
- **URL**: `http://bot-n8n:5678/webhook/evolution`
- **Webhook Base64**: ✅ ligado (necessário para download de áudio)
- **Events**: marque pelo menos `MESSAGES_UPSERT`

> **Importante:** A URL usa `bot-n8n` (nome do container na rede Docker interna), **não** `localhost`.

### 3. Configurar o n8n

#### 3.1 — Acessar o n8n

Abra no navegador: **http://localhost:5678**

Na primeira vez, crie uma conta (dados ficam salvos localmente).

#### 3.2 — Configurar Credencial do Google Gemini

1. Vá em **Settings → Credentials → Add Credential**
2. Busque **"Google Gemini (PaLM) Api"**
3. Cole sua API Key do Google AI Studio
4. Salve

#### 3.3 — Importar o Workflow

1. No n8n, clique em **"Add Workflow" → "Import from File"**
2. Selecione o arquivo `chat-bot-workflow.json` deste repositório
3. **Selecione a credencial do Gemini** no nó "Gemini - Transcrever Áudio"
4. Nos nós **"Download Áudio"** e **"Responder no WhatsApp"**, verifique se os headers contêm `apikey: sua_chave_api_super_secreta`
5. Clique em **"Save"** e depois ative o workflow (toggle no canto superior direito)

### 4. Testar!

1. De outro celular, envie um **áudio** via WhatsApp para o número conectado
2. O bot deve responder com a transcrição em poucos segundos
3. Acompanhe a execução no n8n: **Executions** (menu lateral)

---

## 📋 Estrutura do Workflow n8n

```
Webhook → Filtrar Áudio → Download Áudio → Base64→Binário → Gemini Transcrever → Responder WhatsApp
```

| # | Nó | Tipo | Função |
|---|-----|------|--------|
| 1 | **Webhook Evolution API** | Webhook | Recebe `POST /webhook/evolution` da Evolution API |
| 2 | **Filtrar Mensagens de Áudio** | Code (JS) | Verifica se é `audioMessage`, extrai `messageId` e `remoteJid` |
| 3 | **Download Áudio** | HTTP Request | `POST` para Evolution API `getBase64FromMediaMessage` |
| 4 | **Base64 → Binário** | Code (JS) | Converte áudio base64 para binary data `.ogg` |
| 5 | **Gemini - Transcrever Áudio** | Google Gemini | Transcreve o áudio usando modelo `gemini-2.5-flash` |
| 6 | **Responder no WhatsApp** | HTTP Request | `POST` para Evolution API `sendText` com a transcrição |

---

## 📁 Estrutura do Projeto

```
chatbot/
├── docker-compose.yml          # Infraestrutura (PostgreSQL, Redis, n8n, Evolution API, Nginx)
├── chat-bot-workflow.json      # Workflow n8n (importar no painel)
├── nginx/
│   └── nginx.conf              # Configuração do proxy reverso
├── teste-chatbot/              # Interface web (frontend)
├── chatbot-manguinhos/         # Documentação MkDocs
│   ├── mkdocs.yml
│   └── docs/
└── .specify/                   # Governança e especificações do projeto
```

> 📖 **Documentação completa**: [mare-de-manguinhos.github.io/chatbot](https://mare-de-manguinhos.github.io/chatbot/)

## 📜 Constituição do Projeto

Este repositório adota uma constituição em `.specify/memory/constitution.md` com quatro
princípios obrigatórios:

1. **Confiabilidade do Fluxo**: o pipeline áudio → transcrição → resposta nunca silencia
   erros e sempre retorna mensagem amigável ao pescador.
2. **Infraestrutura como Código**: toda configuração operacional vive em
   `docker-compose.yml` e no repositório.
3. **Baixo Custo Operacional**: prioriza APIs gratuitas (Gemini AI Studio) e exige
   justificativa explícita para serviços pagos.
4. **Extensibilidade Incremental**: novas features entram como nós n8n isolados, sem
   refatoração ampla do fluxo existente.

---

## 🔧 Troubleshooting

### QR Code não aparece

- Verifique os logs: `docker compose logs -f evolution-api`
- Atualize `CONFIG_SESSION_PHONE_VERSION` no `docker-compose.yml` com a versão mais recente de [wppconnect.io/whatsapp-versions](https://wppconnect.io/whatsapp-versions/)
- Reinicie: `docker compose down && docker compose up -d`

### Erro "Invalid url property" ao configurar webhook

- A URL do webhook deve usar **hífens** nos nomes de container (ex: `bot-n8n`), não underscores
- URLs com underscore no hostname são rejeitadas (RFC 952)

### Erro 400 ao responder (Bad Request / exists: false)

- Certifique-se de usar a Evolution API **v2.3.7+** (imagem `evoapicloud/evolution-api`)
- A versão antiga (`atendai/evolution-api`) não suporta o formato **LID** do WhatsApp

### Áudio não é baixado

- Verifique se `DATABASE_SAVE_DATA_NEW_MESSAGE=true` está no `docker-compose.yml`
- Confirme que `Webhook Base64` está ativado nas configurações da instância

### Containers reiniciando

- Verifique logs: `docker compose logs -f`
- O PostgreSQL precisa estar healthy antes dos outros serviços (já configurado com healthcheck)

---

## 🚧 Próximos Passos (Fase 2)

- [ ] Adicionar nó Gemini para **extrair dados estruturados** do áudio (nome do peixe, peso, preço)
- [ ] Retornar dados em formato **JSON** para sistema externo
- [ ] Validação e confirmação dos dados extraídos com o pescador
- [ ] Tratamento de erros e mensagens amigáveis
