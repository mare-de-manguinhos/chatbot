export default function CampoEsperadoRow({ campo, indice, aoAtualizar, aoRemover }) {
  return (
    <div className="campo-esperado-row">
      <input
        type="text"
        placeholder="chave (ex: pescador)"
        value={campo.chave}
        onChange={(e) => aoAtualizar(indice, "chave", e.target.value)}
      />
      <input
        type="text"
        placeholder="valor esperado"
        value={campo.valor}
        onChange={(e) => aoAtualizar(indice, "valor", e.target.value)}
      />
      <button
        type="button"
        className="btn-deletar"
        onClick={() => aoRemover(indice)}
        title="Remover campo"
      >
        ×
      </button>
    </div>
  );
}
