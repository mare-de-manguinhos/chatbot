# Erros Tratados no Bot 

O bot agora detecta falhas nos seguintes pontos e avisa o pescador automaticamente.

###  Erros tratados:
1.  **Download do Áudio**: Erros ao baixar o áudio do WhatsApp.
2.  **Transcrição (Gemini)**: Falhas na inteligência artificial do Google.
3.  **Extração de Dados**: Erros ao tentar organizar as informações (peixe, peso, preço).

### Resposta ao Pescador:
Se qualquer um desses problemas ocorrer, o pescador recebe:
> ⚠️ *Não foi possível completar a operação, tente novamente mais tarde.*

### Como funciona:
Cada nó crítico tem uma "saída de erro" ligada a um comando de envio de mensagem, garantindo que o usuário nunca fique sem resposta.
