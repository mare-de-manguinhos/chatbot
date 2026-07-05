# Bot Pescadores Manguinhos

## Descrição
Bot que recebe áudios de pescadores via WhatsApp, transcreve automaticamente usando **Google Gemini** e extrai dados estruturados de venda (espécie, peso e preço). A orquestração é feita pelo **n8n** e a conexão com WhatsApp pela **Evolution API**.

## Arquitetura

```
Pescador (WhatsApp) → Evolution API → n8n Webhook → Gemini (Transcrição) → Resposta WhatsApp
```

**Stack:**

| Serviço | Descrição | Porta |
|---------|-----------|-------|
| **Evolution API** v2.3.7 | Conexão com WhatsApp Web via Baileys | `8080` |
| **n8n** | Orquestrador de workflow visual | `5678` |
| **Google Gemini** | Transcrição de áudio (gratuito via AI Studio) | — |
| **PostgreSQL** 15 | Banco de dados para n8n e Evolution API | `5432` |
| **Redis** 7 | Cache de sessões WhatsApp | — |

## Estrutura do Projeto

```
chatbot/
├── docker-compose.yml          # Infraestrutura completa (todos os serviços)
├── chat-bot-workflow.json      # Workflow n8n (importar no painel)
├── nginx/
│   └── nginx.conf              # Configuração do proxy reverso
├── teste-chatbot/              # Interface web (frontend)
├── chatbot-manguinhos/         # Documentação MkDocs
│   ├── mkdocs.yml
│   └── docs/
└── .specify/                   # Governança e especificações do projeto
```

## Documentação

A documentação completa está disponível em **[mare-de-manguinhos.github.io/chatbot](https://mare-de-manguinhos.github.io/chatbot/)**.

| Página | Descrição |
|--------|-----------|
| [Visão Geral](https://mare-de-manguinhos.github.io/chatbot/) | Arquitetura, stack de serviços e estrutura do repositório |
| [Para Desenvolvedores](https://mare-de-manguinhos.github.io/chatbot/developer/) | Guia para subir o ambiente local com Docker |
| [Para Clientes](https://mare-de-manguinhos.github.io/chatbot/client/) | Como conectar o WhatsApp e usar o bot |
| [Workflow n8n](https://mare-de-manguinhos.github.io/chatbot/workflow/) | Detalhes de cada nó do fluxo de processamento |
| [Troubleshooting](https://mare-de-manguinhos.github.io/chatbot/troubleshooting/) | Soluções para os erros mais comuns |

## Constituição do Projeto

Este repositório adota uma constituição em `.specify/memory/constitution.md` com quatro princípios obrigatórios:

1. **Confiabilidade do Fluxo** — toda falha retorna mensagem amigável ao pescador; o fluxo nunca silencia erros.
2. **Infraestrutura como Código** — toda configuração operacional vive no `docker-compose.yml` e no repositório.
3. **Baixo Custo Operacional** — prioriza APIs gratuitas (Gemini AI Studio); serviços pagos exigem justificativa explícita.
4. **Extensibilidade Incremental** — novas features entram como nós n8n isolados, sem refatoração ampla do fluxo existente.

<div align="center">

**Equipe:** Allicia Rocha · Guilherme Gomes · Manuely Lemos · Rafael Deps · Thiago Deps  
**Professor:** Paulo Sérgio dos Santos Júnior  
**Ifes Campus Serra** — Extensão em Desenvolvimento de Software

</div>
