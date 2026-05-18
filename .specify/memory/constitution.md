<!--
Sync Impact Report
- Version change: template -> 1.0.0
- Modified principles:
	- [PRINCIPLE_1_NAME] -> I. Confiabilidade do Fluxo
	- [PRINCIPLE_2_NAME] -> II. Infraestrutura como Codigo
	- [PRINCIPLE_3_NAME] -> III. Baixo Custo Operacional
	- [PRINCIPLE_4_NAME] -> IV. Extensibilidade Incremental
- Added sections:
	- Restrições Operacionais
	- Fluxo de Entrega e Qualidade
- Removed sections:
	- [PRINCIPLE_5_NAME]
- Templates requiring updates:
	- .specify/templates/plan-template.md ✅ updated
	- .specify/templates/spec-template.md ✅ updated
	- .specify/templates/tasks-template.md ✅ updated
	- .specify/templates/commands/*.md ⚠ pending (diretorio ausente neste repositorio)
	- README.md ✅ updated
- Follow-up TODOs:
	- None
-->

# Bot Pescadores Manguinhos Constitution

## Core Principles

### I. Confiabilidade do Fluxo
O pipeline audio -> transcricao -> resposta MUST tratar falhas de forma explicita em todos
os nos criticos. Nenhuma excecao, timeout, resposta vazia, falha de rede ou erro de API
MAY encerrar o processamento sem retorno ao pescador. Toda falha MUST resultar em
mensagem amigavel no WhatsApp com orientacao de proxima acao.
Rationale: a experiencia de uso depende de resposta previsivel em campo, mesmo quando
servicos externos falham.

### II. Infraestrutura como Codigo
Toda configuracao operacional MUST ser versionada no repositorio e representada em
docker-compose.yml (servicos, portas, variaveis, healthchecks e dependencias). Ajustes
manuais em ambiente local, servidor ou painel de servico sem registro no repositorio
MUST NOT ser parte do fluxo oficial.
Rationale: reproducibilidade e recuperacao rapida exigem infraestrutura declarativa.

### III. Baixo Custo Operacional
Integracoes MUST priorizar opcoes gratuitas ou ja aprovadas no projeto, com preferencia
por Gemini AI Studio para IA. Introducao de servicos pagos MAY ocorrer somente com
justificativa explicita em documento de decisao, incluindo custo estimado, alternativa
gratuita avaliada e impacto esperado.
Rationale: sustentabilidade financeira e continuidade operacional dependem de custo
controlado.

### IV. Extensibilidade Incremental
Novas capacidades (por exemplo: extracao de dados, validacao ou enriquecimento) MUST ser
adicionadas como nos n8n isolados e claramente delimitados, preservando o caminho
existente do fluxo principal. Refatoracao ampla do fluxo atual MUST NOT ocorrer sem
necessidade comprovada e plano de migracao validado.
Rationale: evolucao incremental reduz risco de regressao em um fluxo de producao ativo.

## Restrições Operacionais

- Fluxos n8n MUST registrar erros tecnicos em logs e retornar mensagem amigavel ao usuario.
- Dependencias externas MUST declarar plano de fallback quando aplicavel.
- Segredos e chaves MUST ser carregados por variaveis de ambiente declaradas no
	docker-compose.yml ou arquivos de ambiente versionados como exemplo.
- Mudancas que alterem custo mensal MUST incluir estimativa de custo antes da aprovacao.

## Fluxo de Entrega e Qualidade

- Toda especificacao de feature MUST citar como atende cada principio desta constituicao.
- Todo plano tecnico MUST conter um Constitution Check com gates objetivos e verificaveis.
- Toda lista de tarefas MUST incluir itens de: tratamento de erro no fluxo, atualizacao de
	infraestrutura declarativa e validacao de custo operacional.
- Revisao de mudanca MUST bloquear merge quando houver violacao sem justificativa aprovada.

## Governance

Esta constituicao prevalece sobre praticas ad hoc do projeto.

- Emendas MUST ser propostas em pull request com: objetivo, impacto, plano de migracao e
	atualizacao dos templates afetados.
- Revisao de conformidade MUST ocorrer em toda PR, verificando aderencia aos quatro
	principios e as restricoes operacionais.
- Versionamento da constituicao MUST seguir SemVer:
	- MAJOR para remocao/redefinicao incompativel de principio ou governanca.
	- MINOR para novo principio, nova secao normativa ou expansao material de regras.
	- PATCH para clarificacoes editoriais sem mudar obrigacoes normativas.
- O arquivo README.md e os templates em .specify/templates MUST permanecer sincronizados
	com esta constituicao.

**Version**: 1.0.0 | **Ratified**: 2026-05-11 | **Last Amended**: 2026-05-11
