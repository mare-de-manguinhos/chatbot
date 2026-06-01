# teste-chatbot

Sistema de testes tipo Postman para o agente n8n de transcrição de áudio (Bot Pescadores).

Cadastre arquivos de áudio e os campos esperados de resposta, execute os testes e veja o resultado campo a campo.

---

## Pré-requisitos

- Python 3.11+
- Node.js 18+
- n8n rodando localmente (via `docker compose up` na raiz do projeto)

---

## 1. Configurar o Workflow de Teste no n8n

1. Acesse o n8n em `http://localhost:5678`
2. Clique em **+ New Workflow → Import from file**
3. Selecione o arquivo `n8n-workflow-teste.json` (está nesta pasta)
4. Configure as credenciais **Google Gemini** nos dois nós que pedem (Gemini - Transcrever Áudio e Google Gemini Chat Model)
5. Clique em **Activate** para ativar o workflow

O webhook ficará disponível em: `http://localhost:5678/webhook/teste-audio`

---

## 2. Instalar dependências do backend

```bash
pip install -r requirements.txt
```

---

## 3. Instalar dependências do frontend

```bash
cd frontend
npm install
cd ..
```

---

## 4. Rodar em desenvolvimento

Abra dois terminais dentro de `teste-chatbot/`:

**Terminal 1 — Backend (FastAPI):**
```bash
uvicorn app.main:app --port 8001 --reload
```

**Terminal 2 — Frontend (React + Vite):**
```bash
cd frontend
npm run dev
```

Acesse: **http://localhost:5173**

> O Vite proxia automaticamente as chamadas `/api` para o FastAPI na porta 8001.

---

## 5. Primeiro uso

1. Abra `http://localhost:5173`
2. Na sidebar esquerda, expanda **⚙ Webhooks** e clique em **+ Novo Webhook**
   - Nome: `Prod` (ou qualquer nome)
   - URL: `http://localhost:5678/webhook/teste-audio`
3. Clique em **+ Novo** na seção Casos de Teste
4. Preencha o nome, selecione o webhook, arraste um arquivo de áudio `.ogg`
5. Adicione os campos esperados (ex: `pescador` → `João Silva`)
6. Clique em **Salvar**
7. Clique em **▶ Executar** — o resultado aparece no painel direito

---

## 6. Rodar os testes automatizados

```bash
pytest app/tests/ -v
```

---

## 7. Build para produção

```bash
cd frontend
npm run build
cd ..
uvicorn app.main:app --port 8001
```

O FastAPI detecta a pasta `frontend/dist/` e serve o frontend em `http://localhost:8001`.

---

## Variáveis de ambiente

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| `URL_BANCO` | `sqlite:///./banco.db` | Caminho do banco SQLite |

---

## Estrutura

```
teste-chatbot/
├── constituicao.md          # Princípios de qualidade do projeto
├── requirements.txt
├── n8n-workflow-teste.json  # Workflow n8n para importar
├── app/
│   ├── models/              # Entidades SQLAlchemy
│   ├── schemas/             # Validação Pydantic
│   ├── repositories/        # Acesso ao banco
│   ├── services/            # Lógica de negócio
│   ├── controllers/         # Rotas FastAPI (thin)
│   └── tests/               # Testes unitários e de integração
└── frontend/                # React + Vite
    └── src/
        ├── components/
        └── services/api.js
```
