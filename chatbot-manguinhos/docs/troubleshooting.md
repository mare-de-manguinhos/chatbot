# Troubleshooting

## QR Code não aparece

- Verifique os logs: `docker compose logs -f evolution-api`
- Atualize `CONFIG_SESSION_PHONE_VERSION` no `docker-compose.yml` com a versão mais recente disponível em [wppconnect.io/whatsapp-versions](https://wppconnect.io/whatsapp-versions/)
- Reinicie: `docker compose down && docker compose up -d`

## Erro "Invalid url property" ao configurar webhook

- A URL do webhook deve usar **hífens** nos nomes de container (ex: `bot-n8n`), não underscores
- URLs com underscore no hostname são rejeitadas pela RFC 952

## Erro 400 ao responder (Bad Request / exists: false)

- Use a Evolution API **v2.3.7+** (imagem `evoapicloud/evolution-api`)
- A versão antiga (`atendai/evolution-api`) não suporta o formato **LID** do WhatsApp

## Áudio não é baixado

- Confirme que `DATABASE_SAVE_DATA_NEW_MESSAGE=true` está no `docker-compose.yml`
- Confirme que **Webhook Base64** está ativado nas configurações da instância Evolution API

## Containers reiniciando em loop

- Verifique os logs: `docker compose logs -f`
- O PostgreSQL deve estar `healthy` antes dos outros serviços — o `healthcheck` já está configurado no `docker-compose.yml`
- Se o problema persistir, remova os volumes e reinicie: `docker compose down -v && docker compose up -d`

!!! warning
    `docker compose down -v` apaga todos os dados persistidos (banco, sessões WhatsApp, workflows do n8n). Use apenas em ambiente de desenvolvimento.

## n8n não recebe as mensagens

1. Confirme que a instância está **Connected** no painel da Evolution API
2. Confirme que o webhook está configurado e habilitado na instância
3. Confirme que o workflow está **ativo** no n8n (toggle verde no canto superior direito)
4. Verifique os logs do n8n: `docker compose logs -f n8n`
