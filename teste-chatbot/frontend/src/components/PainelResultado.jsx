import { useState, useEffect } from "react";

const COR_STATUS = {
  aprovado: "status-aprovado",
  reprovado: "status-reprovado",
  erro: "status-erro",
  executando: "status-executando",
};

const LABEL_STATUS = {
  aprovado: "✅ APROVADO",
  reprovado: "❌ REPROVADO",
  erro: "⚠️ ERRO",
  executando: "⏳ EXECUTANDO...",
};

export default function PainelResultado({ execucao, carregando }) {
  const [comparacao, setComparacao] = useState(null);
  const [jsonObtido, setJsonObtido] = useState(null);

  useEffect(() => {
    if (!execucao) {
      setComparacao(null);
      setJsonObtido(null);
      return;
    }
    try {
      if (execucao.resultado_comparacao) {
        setComparacao(JSON.parse(execucao.resultado_comparacao));
      }
      if (execucao.json_obtido) {
        setJsonObtido(JSON.parse(execucao.json_obtido));
      }
    } catch {}
  }, [execucao]);

  if (carregando) {
    return (
      <div className="painel-resultado">
        <div className="resultado-vazio">
          <span className="status-executando">⏳ Executando teste...</span>
        </div>
      </div>
    );
  }

  if (!execucao) {
    return (
      <div className="painel-resultado">
        <div className="resultado-vazio">
          <p>Selecione um caso e clique em <strong>▶ Executar</strong> para ver o resultado.</p>
        </div>
      </div>
    );
  }

  const classStatus = COR_STATUS[execucao.status] || "";
  const labelStatus = LABEL_STATUS[execucao.status] || execucao.status;

  return (
    <div className="painel-resultado">
      <div className={`resultado-status ${classStatus}`}>
        <span className="label-status">{labelStatus}</span>
        {execucao.duracao_ms > 0 && (
          <span className="duracao">{(execucao.duracao_ms / 1000).toFixed(1)}s</span>
        )}
      </div>

      {execucao.mensagem_erro && (
        <div className="resultado-erro">
          <strong>Erro:</strong> {execucao.mensagem_erro}
        </div>
      )}

      {comparacao && comparacao.falhas && (
        <div className="resultado-comparacao">
          <h3>Comparação de Campos</h3>
          <table className="tabela-comparacao">
            <thead>
              <tr>
                <th>Chave</th>
                <th>Esperado</th>
                <th>Obtido</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {comparacao.falhas.map((f) => (
                <tr key={f.chave} className="linha-falha">
                  <td>{f.chave}</td>
                  <td>{f.esperado}</td>
                  <td>{f.obtido ?? "—"}</td>
                  <td>❌</td>
                </tr>
              ))}
              {jsonObtido && execucao.status !== "erro" &&
                Object.entries(jsonObtido)
                  .filter(([chave]) => !comparacao.falhas.find((f) => f.chave === chave))
                  .filter(([chave]) => chave !== "transcricao")
                  .map(([chave, valor]) => (
                    <tr key={chave} className="linha-passou">
                      <td>{chave}</td>
                      <td>—</td>
                      <td>{String(valor)}</td>
                      <td>✅</td>
                    </tr>
                  ))}
            </tbody>
          </table>
        </div>
      )}

      {execucao.transcricao_obtida && (
        <div className="resultado-transcricao">
          <h3>Transcrição</h3>
          <p>{execucao.transcricao_obtida}</p>
        </div>
      )}

      {jsonObtido && (
        <details className="resultado-json-bruto">
          <summary>JSON completo recebido</summary>
          <pre>{JSON.stringify(jsonObtido, null, 2)}</pre>
        </details>
      )}
    </div>
  );
}
