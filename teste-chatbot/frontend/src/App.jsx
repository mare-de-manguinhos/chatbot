import { useState, useEffect } from "react";
import ListaCasos from "./components/ListaCasos.jsx";
import ListaWebhooks from "./components/ListaWebhooks.jsx";
import FormularioCaso from "./components/FormularioCaso.jsx";
import PainelResultado from "./components/PainelResultado.jsx";
import { casos as apiCasos, execucoes as apiExecucoes } from "./services/api.js";

export default function App() {
  const [listaCasos, setListaCasos] = useState([]);
  const [casoSelecionado, setCasoSelecionado] = useState(null);
  const [ultimaExecucao, setUltimaExecucao] = useState(null);
  const [executandoTodos, setExecutandoTodos] = useState(false);
  const [sumario, setSumario] = useState(null);
  const [carregando, setCarregando] = useState(false);

  async function carregarCasos() {
    try {
      const dados = await apiCasos.listar();
      setListaCasos(dados);
    } catch (erro) {
      console.error("Erro ao carregar casos:", erro);
    }
  }

  useEffect(() => {
    carregarCasos();
  }, []);

  async function aoSelecionarCaso(caso) {
    setCasoSelecionado(caso);
    setUltimaExecucao(null);
    try {
      const execucoesDoCaso = await apiExecucoes.listarDoCaso(caso.id);
      if (execucoesDoCaso.length > 0) {
        setUltimaExecucao(execucoesDoCaso[0]);
      }
    } catch {}
  }

  async function aoExecutarTodos() {
    setExecutandoTodos(true);
    setSumario(null);
    try {
      const resultado = await apiExecucoes.executarTodos();
      setSumario(resultado);
      await carregarCasos();
    } catch (erro) {
      alert(`Erro ao executar todos: ${erro.message}`);
    } finally {
      setExecutandoTodos(false);
    }
  }

  async function aoExecutarCaso(casoId) {
    setCarregando(true);
    try {
      const execucao = await apiExecucoes.executar(casoId);
      setUltimaExecucao(execucao);
      await carregarCasos();
    } catch (erro) {
      alert(`Erro ao executar: ${erro.message}`);
    } finally {
      setCarregando(false);
    }
  }

  const aprovados = listaCasos.filter((c) => c.ultimo_status === "aprovado").length;
  const reprovados = listaCasos.filter((c) => c.ultimo_status === "reprovado").length;

  return (
    <div className="app">
      <header className="cabecalho">
        <div className="cabecalho-titulo">
          <span className="logo">🎣</span>
          <h1>teste-chatbot</h1>
        </div>
        <div className="cabecalho-acoes">
          {sumario && (
            <span className="sumario">
              {sumario.aprovados}✅ · {sumario.reprovados}❌ · {sumario.erros}⚠️
            </span>
          )}
          {!sumario && listaCasos.length > 0 && (
            <span className="sumario">
              {aprovados}✅ · {reprovados}❌
            </span>
          )}
          <button
            className="btn-primario"
            onClick={aoExecutarTodos}
            disabled={executandoTodos || listaCasos.length === 0}
          >
            {executandoTodos ? "⏳ Executando..." : "▶ Executar Todos"}
          </button>
        </div>
      </header>

      <main className="painel-principal">
        <aside className="sidebar">
          <ListaCasos
            casos={listaCasos}
            casoSelecionado={casoSelecionado}
            aoSelecionar={aoSelecionarCaso}
            aoAtualizar={carregarCasos}
          />
          <ListaWebhooks />
        </aside>

        <section className="area-formulario">
          <FormularioCaso
            caso={casoSelecionado}
            aoSalvar={async () => {
              await carregarCasos();
              setCasoSelecionado(null);
            }}
            aoExecutar={aoExecutarCaso}
            carregando={carregando}
          />
        </section>

        <section className="area-resultado">
          <PainelResultado execucao={ultimaExecucao} carregando={carregando} />
        </section>
      </main>
    </div>
  );
}
