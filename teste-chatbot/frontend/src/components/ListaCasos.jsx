import { casos as apiCasos } from "../services/api.js";

const ICONE_STATUS = {
  aprovado: "✅",
  reprovado: "❌",
  erro: "⚠️",
};

export default function ListaCasos({ casos, casoSelecionado, aoSelecionar, aoAtualizar }) {
  async function aoDeletar(e, casoId) {
    e.stopPropagation();
    if (!confirm("Remover este caso de teste?")) return;
    try {
      await apiCasos.deletar(casoId);
      await aoAtualizar();
    } catch (erro) {
      alert(`Erro ao remover: ${erro.message}`);
    }
  }

  return (
    <div className="secao-sidebar">
      <div className="secao-sidebar-cabecalho">
        <h2>Casos de Teste</h2>
        <button className="btn-secundario btn-pequeno" onClick={() => aoSelecionar(null)}>
          + Novo
        </button>
      </div>
      <ul className="lista-casos">
        {casos.length === 0 && (
          <li className="lista-vazia">Nenhum caso cadastrado</li>
        )}
        {casos.map((caso) => (
          <li
            key={caso.id}
            className={`item-caso ${casoSelecionado?.id === caso.id ? "selecionado" : ""}`}
            onClick={() => aoSelecionar(caso)}
          >
            <span className="icone-status">
              {ICONE_STATUS[caso.ultimo_status] || "⬜"}
            </span>
            <span className="nome-caso">{caso.nome}</span>
            <button
              className="btn-deletar"
              onClick={(e) => aoDeletar(e, caso.id)}
              title="Remover"
            >
              ×
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
