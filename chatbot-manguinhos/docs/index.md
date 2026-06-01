# Bot Pescadores Manguinhos

Bot que recebe áudios de pescadores via WhatsApp, transcreve automaticamente com **Google Gemini** e extrai dados estruturados de venda (espécie, peso e preço). A orquestração é feita pelo **n8n** e a conexão com WhatsApp pela **Evolution API**.

---

## Arquitetura

```
Pescador (WhatsApp)
       │
       ▼
  Evolution API  ←── gerencia sessão WhatsApp
       │
       ▼ webhook (POST)
      n8n  ←── orquestra o fluxo
       │
       ▼
 Google Gemini  ←── transcreve o áudio
       │
       ▼
 Resposta WhatsApp
```

## Stack de Serviços

| Serviço | Função | Porta |
|---------|--------|-------|
| **Evolution API** v2.3.7 | Conexão com WhatsApp via Baileys | `8080` |
| **n8n** | Orquestrador visual de workflows | `5678` |
| **Google Gemini** | Transcrição de áudio via AI Studio (gratuito) | — |
| **PostgreSQL** 15 | Banco de dados para n8n e Evolution API | `5432` |
| **Redis** 7 | Cache de sessões WhatsApp | — |
| **Nginx** | Proxy reverso para a interface web | `80` |

## Estrutura do Repositório

```
chatbot/
├── docker-compose.yml        # Infraestrutura completa (todos os serviços)
├── chat-bot-workflow.json    # Workflow n8n (importar no painel)
├── nginx/
│   └── nginx.conf            # Configuração do proxy reverso
├── teste-chatbot/            # Interface web (frontend)
├── chatbot-manguinhos/       # Esta documentação (MkDocs)
└── .specify/                 # Governança e especificações do projeto
```

## Princípios do Projeto

| Princípio | Descrição |
|-----------|-----------|
| **Confiabilidade do Fluxo** | Toda falha retorna mensagem amigável ao pescador — o fluxo nunca silencia erros |
| **Infraestrutura como Código** | Toda configuração vive no `docker-compose.yml` e no repositório |
| **Baixo Custo Operacional** | Prioriza APIs gratuitas (Gemini AI Studio); serviços pagos exigem justificativa |
| **Extensibilidade Incremental** | Novas capacidades entram como nós n8n isolados, sem refatorar o fluxo existente |
