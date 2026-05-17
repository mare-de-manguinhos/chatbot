const BASE_URL = "/api";

async function requisitar(metodo, caminho, corpo) {
  const opcoes = { method: metodo };
  if (corpo instanceof FormData) {
    opcoes.body = corpo;
  } else if (corpo) {
    opcoes.headers = { "Content-Type": "application/json" };
    opcoes.body = JSON.stringify(corpo);
  }
  const resposta = await fetch(`${BASE_URL}${caminho}`, opcoes);
  if (!resposta.ok) {
    const erro = await resposta.json().catch(() => ({ detail: resposta.statusText }));
    throw new Error(erro.detail || "Erro na requisição");
  }
  if (resposta.status === 204) return null;
  return resposta.json();
}

// Webhooks
export const webhooks = {
  listar: () => requisitar("GET", "/webhooks/"),
  criar: (dados) => requisitar("POST", "/webhooks/", dados),
  atualizar: (id, dados) => requisitar("PUT", `/webhooks/${id}`, dados),
  deletar: (id) => requisitar("DELETE", `/webhooks/${id}`),
};

// Casos de Teste
export const casos = {
  listar: () => requisitar("GET", "/casos/"),
  buscar: (id) => requisitar("GET", `/casos/${id}`),
  criar: (formData) => requisitar("POST", "/casos/", formData),
  atualizar: (id, formData) => requisitar("PUT", `/casos/${id}`, formData),
  deletar: (id) => requisitar("DELETE", `/casos/${id}`),
};

// Execuções
export const execucoes = {
  executar: (casoId) => requisitar("POST", `/casos/${casoId}/executar`),
  executarTodos: () => requisitar("POST", "/execucoes/executar-todos"),
  listarDoCaso: (casoId) => requisitar("GET", `/casos/${casoId}/execucoes`),
  buscar: (id) => requisitar("GET", `/execucoes/${id}`),
};
