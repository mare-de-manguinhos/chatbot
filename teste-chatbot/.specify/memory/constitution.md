# Constituição do teste-chatbot

Define padrões de qualidade, stack, arquitetura e expectativas de UX.
Não contém regras de negócio.

## Princípios

### I. Código em Português Brasileiro

Variáveis, funções, classes, comentários e strings exibidas ao usuário DEVEM ser escritas
em pt-BR. Exceções permitidas:

- Nomes de pastas e arquivos seguem a convenção do ecossistema (`models/`, `services/`,
  `repositories/`, `controllers/`, `app.js`, `vite.config.js`)
- Keywords de linguagem (`class`, `def`, `return`, `import`)
- Nomes de frameworks e bibliotecas (`FastAPI`, `SQLAlchemy`, `Pydantic`, `React`, `Vite`)
- Termos técnicos sem equivalente consolidado em pt-BR (`id`, `status`, `schema`,
  `payload`, `endpoint`, `webhook`, `base64`, `timeout`)

### II. Stack Definida: FastAPI + SQLAlchemy + React + Vite

- Backend DEVE usar **FastAPI** como framework web
- Persistência DEVE usar **SQLAlchemy** como ORM com **SQLite** em desenvolvimento
- Schemas de entrada e saída DEVEM usar **Pydantic** (integrado ao FastAPI)
- Frontend DEVE usar **React** com **Vite** como bundler
- Em produção, o FastAPI serve o `/dist` gerado pelo `vite build` via `StaticFiles`
- Em desenvolvimento, o Vite roda em porta separada e proxia `/api` para o FastAPI
- Nenhum outro framework, ORM ou bundler MAY ser introduzido sem emenda a esta
  constituição

### III. Arquitetura em 5 Camadas

O sistema DEVE ser organizado nas camadas abaixo. Violações de fronteira (ex: lógica de
negócio em controller, query SQL em service) NÃO DEVEM ocorrer.

| Camada | Pasta | Responsabilidade |
|--------|-------|-----------------|
| **Model** | `app/models/` | Definição das entidades ORM (SQLAlchemy). Sem lógica. |
| **Repository** | `app/repositories/` | Consultas e persistência. Recebe `Session`, retorna models ou `None`. Sem lógica de negócio. |
| **Service** | `app/services/` | Lógica de negócio e orquestração. Chama repositories. NÃO acessa `Session` diretamente — usa repositories. |
| **Controller** | `app/controllers/` | Thin. Parseia request via schema Pydantic, chama service, retorna response. Sem lógica. Regra: controller sem `import Session` é saudável. |
| **View** | `frontend/` | React + Vite. Consome a API REST via `fetch`. Build em `frontend/dist/`. |

### IV. Política de Testes do Próprio Projeto

- Services core (`comparador`, `cliente_n8n`) DEVEM ter testes unitários cobrindo o
  caminho feliz e pelo menos um caminho de erro
- Controllers DEVEM ter pelo menos 1 teste de integração por rota
- Testes ficam em `app/tests/`
- Código sem teste correspondente NÃO é considerado entregue

### V. Expectativas de UX

- A interface DEVE ser utilizável sem documentação por um desenvolvedor que nunca a viu
- Toda ação assíncrona (chamada de API, execução de teste) DEVE exibir estado de
  carregamento visível
- Resultados DEVEM ser visualmente distinguíveis:
  - Aprovado → verde
  - Reprovado → vermelho
  - Erro → amarelo/laranja
- Nenhum fluxo primário (cadastrar webhook, criar caso de teste, executar teste, ver
  resultado) DEVE exigir mais de 3 interações do usuário

## Entidades do Sistema

O sistema possui exatamente 3 entidades principais:

| Entidade | Descrição |
|----------|-----------|
| `Webhook` | URL de webhook n8n registrada para receber áudio de teste |
| `CasoDeTeste` | Áudio + campos esperados associados a um webhook |
| `Execucao` | Resultado de uma execução de um caso de teste |

`CampoEsperado` é uma entidade de apoio (par chave/valor) que pertence a `CasoDeTeste`.

Para cada entidade principal DEVE existir: model, repository, service e controller
correspondentes.

## Governança

Esta constituição prevalece sobre práticas ad hoc.

- Emendas DEVEM ser propostas via PR com: objetivo, impacto e atualização deste documento
- Revisão de conformidade DEVE ocorrer em toda PR
- Versionamento segue SemVer:
  - MAJOR: remoção ou redefinição incompatível de princípio
  - MINOR: novo princípio ou nova seção normativa
  - PATCH: clarificações editoriais sem mudança de obrigações

**Versão**: 1.0.0 | **Ratificada**: 2026-05-17
