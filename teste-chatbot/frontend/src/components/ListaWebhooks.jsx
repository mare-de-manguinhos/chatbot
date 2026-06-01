import { useState, useEffect } from "react";
import { webhooks as apiWebhooks } from "../services/api.js";

export default function ListaWebhooks() {
  const [listaWebhooks, setListaWebhooks] = useState([]);
  const [expandido, setExpandido] = useState(false);
  const [criando, setCriando] = useState(false);
  const [novoNome, setNovoNome] = useState("");
  const [novaUrl, setNovaUrl] = useState("");
  const [salvando, setSalvando] = useState(false);

  async function carregar() {
    try {
      const dados = await apiWebhooks.listar();
      setListaWebhooks(dados);
    } catch {}
  }

  useEffect(() => {
    carregar();
  }, []);

  async function aoSalvarWebhook(e) {
    e.preventDefault();
    if (!novoNome.trim() || !novaUrl.trim()) return;
    setSalvando(true);
    try {
      await apiWebhooks.criar({ nome: novoNome, url: novaUrl });
      setNovoNome("");
      setNovaUrl("");
      setCriando(false);
      await carregar();
    } catch (erro) {
      alert(`Erro ao salvar webhook: ${erro.message}`);
    } finally {
      setSalvando(false);
    }
  }

  async function aoDeletar(id) {
    if (!confirm("Remover este webhook?")) return;
    try {
      await apiWebhooks.deletar(id);
      await carregar();
    } catch (erro) {
      alert(`Erro ao remover: ${erro.message}`);
    }
  }

  return (
    <div className="secao-sidebar secao-webhooks">
      <div
        className="secao-sidebar-cabecalho clicavel"
        onClick={() => setExpandido(!expandido)}
      >
        <h2>⚙ Webhooks</h2>
        <span>{expandido ? "▲" : "▼"}</span>
      </div>

      {expandido && (
        <div className="conteudo-webhooks">
          <ul className="lista-webhooks">
            {listaWebhooks.map((wh) => (
              <li key={wh.id} className="item-webhook">
                <div className="webhook-info">
                  <span className="webhook-nome">{wh.nome}</span>
                  <span className="webhook-url">{wh.url}</span>
                </div>
                <button
                  className="btn-deletar"
                  onClick={() => aoDeletar(wh.id)}
                  title="Remover"
                >
                  ×
                </button>
              </li>
            ))}
          </ul>

          {criando ? (
            <form className="form-novo-webhook" onSubmit={aoSalvarWebhook}>
              <input
                type="text"
                placeholder="Nome (ex: Prod)"
                value={novoNome}
                onChange={(e) => setNovoNome(e.target.value)}
                required
              />
              <input
                type="url"
                placeholder="URL do webhook"
                value={novaUrl}
                onChange={(e) => setNovaUrl(e.target.value)}
                required
              />
              <div className="form-acoes">
                <button type="submit" className="btn-primario btn-pequeno" disabled={salvando}>
                  {salvando ? "Salvando..." : "Salvar"}
                </button>
                <button type="button" className="btn-secundario btn-pequeno" onClick={() => setCriando(false)}>
                  Cancelar
                </button>
              </div>
            </form>
          ) : (
            <button className="btn-secundario btn-pequeno btn-bloco" onClick={() => setCriando(true)}>
              + Novo Webhook
            </button>
          )}
        </div>
      )}
    </div>
  );
}
