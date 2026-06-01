# Para Clientes

Guia de uso do sistema já implantado. Nenhuma instalação é necessária — basta um navegador e um celular com WhatsApp.

## Endereços do Sistema

| Serviço | Endereço |
|---------|----------|
| **Evolution API** (gerenciador WhatsApp) | `http://163.176.152.188:8080/manager` |
| **n8n** (orquestrador — só equipe técnica) | `http://163.176.152.188:5678` |

---

## Passo 1 — Conectar o WhatsApp

Acesse o gerenciador da Evolution API no navegador:

```
http://163.176.152.188:8080/manager
```

### 1.1 — Criar a instância do cliente

1. Clique em **"Create Instance"**
2. Dê um nome à instância (ex: nome do cliente ou ponto de venda)
3. **Integration**: selecione `WHATSAPP-BAILEYS`
4. Clique em **"Create"**

### 1.2 — Gerar o QR Code

1. Com a instância criada, clique em **"Connect"**
2. Um QR Code será exibido na tela

### 1.3 — Escanear com o WhatsApp

No celular que será usado pelo cliente:

1. Abra o **WhatsApp**
2. Vá em **Configurações → Dispositivos Vinculados → Vincular Dispositivo**
3. Aponte a câmera para o QR Code exibido no navegador

Pronto. A partir desse momento, todas as mensagens recebidas nesse número serão processadas automaticamente pelo n8n.

---

## Passo 2 — Usar o Bot

Com o WhatsApp conectado, o cliente pode enviar **áudios** para o número vinculado seguindo este padrão:

!!! example "Padrão da mensagem de venda"
    **Espécie do peixe, Peso disponível para venda, Preço por quilo**

    Exemplo: *"Robalo, cinco quilos, trinta reais o quilo"*

O n8n recebe o áudio, transcreve com o Google Gemini e processa os dados da venda automaticamente.

---

## O que acontece por baixo

```
Cliente fala no WhatsApp
        │
        ▼
Evolution API recebe a mensagem e envia para o n8n via webhook
        │
        ▼
n8n baixa o áudio e envia para o Google Gemini transcrever
        │
        ▼
Os dados (espécie, peso, preço) são extraídos da transcrição
        │
        ▼
O bot responde no WhatsApp confirmando o registro
```

---

## Dúvidas Frequentes

**O QR Code expirou antes de escanear?**
Clique em **"Connect"** novamente na instância para gerar um novo QR Code.

**A instância ficou desconectada (offline)?**
Acesse `http://163.176.152.188:8080/manager`, localize a instância e clique em **"Connect"** para reconectar.

**O bot não respondeu minha mensagem?**
Verifique se o áudio seguiu o padrão correto: espécie, peso e preço. Mensagens de texto ou outros formatos são ignoradas.
