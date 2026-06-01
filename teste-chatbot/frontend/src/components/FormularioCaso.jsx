import { useState, useEffect, useRef } from "react";
import { webhooks as apiWebhooks, casos as apiCasos } from "../services/api.js";
import CampoEsperadoRow from "./CampoEsperadoRow.jsx";

const CAMPOS_VAZIOS = [{ chave: "", valor: "" }];

export default function FormularioCaso({ caso, aoSalvar, aoExecutar, carregando }) {
  const [listaWebhooks, setListaWebhooks] = useState([]);
  const [nome, setNome] = useState("");
  const [descricao, setDescricao] = useState("");
  const [webhookId, setWebhookId] = useState("");
  const [campos, setCampos] = useState(CAMPOS_VAZIOS);
  const [arquivoAudio, setArquivoAudio] = useState(null);
  const [salvando, setSalvando] = useState(false);
  const refAudio = useRef(null);
  const refInput = useRef(null);

  useEffect(() => {
    apiWebhooks.listar().then(setListaWebhooks).catch(() => {});
  }, []);

  useEffect(() => {
    if (caso) {
      setNome(caso.nome || "");
      setDescricao(caso.descricao || "");
      setWebhookId(caso.webhook_id || "");
      setCampos(caso.campos_esperados?.length > 0 ? caso.campos_esperados : CAMPOS_VAZIOS);
      setArquivoAudio(null);
    } else {
      setNome("");
      setDescricao("");
      setWebhookId(listaWebhooks[0]?.id || "");
      setCampos(CAMPOS_VAZIOS);
      setArquivoAudio(null);
    }
  }, [caso]);

  function atualizarCampo(indice, chave, valor) {
    setCampos((ant) => ant.map((c, i) => (i === indice ? { ...c, [chave]: valor } : c)));
  }

  function adicionarCampo() {
    setCampos((ant) => [...ant, { chave: "", valor: "" }]);
  }

  function removerCampo(indice) {
    setCampos((ant) => ant.filter((_, i) => i !== indice));
  }

  function aoSoltarAudio(e) {
    e.preventDefault();
    const arquivo = e.dataTransfer?.files[0] || e.target.files[0];
    if (arquivo) setArquivoAudio(arquivo);
  }

  async function aoSubmeter(e) {
    e.preventDefault();
    if (!caso && !arquivoAudio) {
      alert("Selecione um arquivo de áudio");
      return;
    }

    const camposValidos = campos.filter((c) => c.chave.trim() && c.valor.trim());
    const formData = new FormData();
    formData.append("nome", nome);
    formData.append("webhook_id", webhookId);
    if (descricao) formData.append("descricao", descricao);
    formData.append("campos_esperados", JSON.stringify(camposValidos));
    if (arquivoAudio) formData.append("arquivo_audio", arquivoAudio);

    setSalvando(true);
    try {
      if (caso) {
        await apiCasos.atualizar(caso.id, formData);
      } else {
        await apiCasos.criar(formData);
      }
      await aoSalvar();
    } catch (erro) {
      alert(`Erro ao salvar: ${erro.message}`);
    } finally {
      setSalvando(false);
    }
  }

  const nomeArquivoExibido = arquivoAudio?.name || caso?.nome_arquivo_audio;

  return (
    <div className="formulario-caso">
      <h2>{caso ? "Editar Caso" : "Novo Caso de Teste"}</h2>

      <form onSubmit={aoSubmeter}>
        <div className="campo-form">
          <label>Nome *</label>
          <input
            type="text"
            value={nome}
            onChange={(e) => setNome(e.target.value)}
            placeholder="ex: Corvina 5kg João"
            required
          />
        </div>

        <div className="campo-form">
          <label>Descrição</label>
          <input
            type="text"
            value={descricao}
            onChange={(e) => setDescricao(e.target.value)}
            placeholder="Opcional"
          />
        </div>

        <div className="campo-form">
          <label>Webhook *</label>
          <select value={webhookId} onChange={(e) => setWebhookId(e.target.value)} required>
            <option value="">Selecione um webhook</option>
            {listaWebhooks.map((wh) => (
              <option key={wh.id} value={wh.id}>
                {wh.nome}
              </option>
            ))}
          </select>
        </div>

        <div className="campo-form">
          <label>Áudio {!caso && "*"}</label>
          <div
            className={`zona-upload ${arquivoAudio ? "com-arquivo" : ""}`}
            onDrop={aoSoltarAudio}
            onDragOver={(e) => e.preventDefault()}
            onClick={() => refInput.current?.click()}
          >
            <input
              ref={refInput}
              type="file"
              accept="audio/*,.ogg,.mp3,.wav"
              style={{ display: "none" }}
              onChange={aoSoltarAudio}
            />
            {nomeArquivoExibido ? (
              <div className="arquivo-selecionado">
                <span>🎵 {nomeArquivoExibido}</span>
                {arquivoAudio && (
                  <audio ref={refAudio} controls src={URL.createObjectURL(arquivoAudio)} />
                )}
              </div>
            ) : (
              <span className="texto-upload">🎵 Arraste o áudio aqui ou clique para selecionar</span>
            )}
          </div>
        </div>

        <div className="campo-form">
          <label>Campos Esperados</label>
          <div className="lista-campos">
            {campos.map((campo, i) => (
              <CampoEsperadoRow
                key={i}
                campo={campo}
                indice={i}
                aoAtualizar={atualizarCampo}
                aoRemover={removerCampo}
              />
            ))}
            <button type="button" className="btn-secundario btn-pequeno" onClick={adicionarCampo}>
              + Adicionar campo
            </button>
          </div>
        </div>

        <div className="form-acoes">
          <button type="submit" className="btn-secundario" disabled={salvando}>
            {salvando ? "Salvando..." : "Salvar"}
          </button>
          {caso && (
            <button
              type="button"
              className="btn-primario"
              onClick={() => aoExecutar(caso.id)}
              disabled={carregando}
            >
              {carregando ? "⏳ Executando..." : "▶ Executar"}
            </button>
          )}
        </div>
      </form>
    </div>
  );
}
