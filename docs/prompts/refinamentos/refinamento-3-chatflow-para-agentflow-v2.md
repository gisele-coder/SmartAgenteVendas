# Refinamento 3 — Chatflow rejeita Chat Model: migração para Agentflow V2

**Data:** 2026-08-31 · **Fase:** 8 (Flowise Low-Code)

## Problema Observado

O roteiro original da Parte 8 previa a topologia de **Chatflow** `ChatPrompt → ChatOpenRouter → Custom Function` no Flowise Cloud. Ao montar o fluxo no editor, o usuário reportou:

> "Já configurei o Custom JS Function, quando tento conectar o output do OpenRouter com o Input do Custom JS Function dá erro de Json"

Reprodução 100 % consistente: o Flowise rejeita a conexão do `ChatOpenRouter` (anchor de saída) para o `Custom Function` (anchor de entrada), exibindo erro de **JSON**. A tentativa ficou registrada em `docs/evidencias/screenshots/flowise-1-erro-conexao-chatflow.jpg`.

## Investigação (causa raiz)

Leitura do código-fonte atual do Flowise (`packages/components/nodes/utilities/CustomFunction/CustomFunction.ts`, v3.0 no branch `main`):

```ts
this.inputs = [
  { label: 'Input Variables', name: 'functionInputVariables',
    type: 'json', optional: true, acceptVariable: true, list: true },
  { label: 'Function Name',  name: 'functionName',         type: 'string', ... },
  { label: 'Additional Tools', name: 'tools',              type: 'Tool',   list: true, optional: true },
  { label: 'Javascript Function', name: 'javascriptFunction', type: 'code' }
]
```

- O node **Custom JS Function** de Chatflow (v3.x) **não tem nenhum anchor de entrada que aceite Chat Model ou Chain** — a única entrada conectável é `Input Variables`, tipada como `json`
- A saída de um Chat Model declara `baseClasses: ['BaseChatModel', 'BaseLanguageModel', ...]` — não há interseção com `json`, por isso a UI rejeita a conexão com erro de JSON
- A topologia antiga do roteiro (válida em versões anteriores do node, hoje removida) não é mais reproduzível na instância atual do Flowise Cloud

## Alteração Realizada

- **Migração de Chatflow V1 → Agentflow V2** no Flowise Cloud (`Start → LLM → Custom Function`)
  - **Start** recebe o payload `{"question": <evento-json>}` enviado pela app (`POST /recomendacoes` → `notify_flowise`)
  - **LLM** (categoria *Agent Flows*): `ChatOpenRouter` (credencial `OpenRouter`), `modelName: poolside/laguna-s-2.1`, `temperature: 0.2`, **System Message** com o prompt SRE (severidade/causa/ação). A entrada humana é o output do Start — não há node de ChatPrompt
  - **Custom Function** (categoria *Agent Flows* — não o de Utilities): código com `require('axios')` (lib garantida no agentflow) que faz `POST $vars.DISCORD_WEBHOOK_URL` com `$input` (saída do LLM)
  - **Variável** `DISCORD_WEBHOOK_URL` criada em **Dashboard → Variables** (não via node Set Variable), acessível via `$vars`
- **Nenhuma alteração no código Python** da app — o `notify_flowise()` continua chamando o mesmo endpoint `POST /api/v1/prediction/<id>`, apenas o **id** agora é de um agentflow
- Documentação reescrita para refletir a nova topologia:
  - [`docs/lowcode/reproducao-flowise.md`](../../lowcode/reproducao-flowise.md) — passo 2 reescrito com roteiro item-a-item (usuário não conhecia a ferramenta); passo 3 com `.env` real deste projeto
  - [`README.md`](../../../README.md) (linha 101–103) — corrigida menção desatualizada "ChatOpenAI Custom (hy3-free via gateway OpenCode)" → "Agentflow V2 (Start → LLM ChatOpenRouter free → Custom Function)"
  - [`docs/plano-execucao.md`](../../plano-execucao.md) — Parte 8 → ✅ Concluída; histórico 31/08
  - [`CHANGELOG.md`](../../../CHANGELOG.md) — `0.8.0` ✅; nova decisão registrada; foco em Parte 9
- Commit semântico na `develop`:
  - `43ec8da` docs: migra roteiro Flowise de chatflow para Agentflow V2
  - `87960dc` feat: conclui integracao low-code flowise com evidencia e2e (parte 8)

## Resultado Obtido

**Demo end-to-end real** (`request_id: 3bfceacea49f`):

| Sinal | Valor |
|---|---|
| Status da requisição | `200` com `status: "blocked"` (security_check bloqueou em 0,1 ms) |
| Latência total da requisição | 10 115 ms |
| `flowise_notify` no `logs/execution.log` | `latency_ms: 6692.3`, `event: security_blocked`, `status_code: 200` |
| Tempo do LLM no Flowise | 1 477 ms (`poolside/laguna-s-2.1`, 348 tokens) |
| Webhook do Discord | **HTTP 204** (alerta entregue) |
| Audit JSONL | 4 eventos correlacionados por `request_id` (`input_validated`, `security_blocked`, `request_blocked`, `response_completed`) |
| Alerta classificado pelo LLM | `SEVERIDADE: alta / EVENTO: security_blocked \| REQUEST: 3bfceacea49f \| CLIENTE: 100011 / CAUSA PROVÁVEL: Tentativa de injeção... / AÇÃO RECOMENDADA: Investigar o payload e validar WAF` |
| Alerta visual no canal `#smartorder-alertas` | ✅ confirmado pelo usuário (screenshot `discord0.jpeg`) |

Confirmação adicional (Parte 5): o **LLM é o gargalo em dois níveis** (app principal e agentflow), reforçando a decisão de mitigação via `flowise_timeout_s=45` e fallback.

## Evidência

- Fluxo versionado (sem segredos): [`docs/lowcode/flowise-flow.json`](../../lowcode/flowise-flow.json) — 3 nodes, 2 edges, grep `discord.com/api/webhooks/[0-9]`, `sk-or`, `Bearer`: **0 matches**
- Evidência completa: [`docs/evidencias/execucoes/flowise-discord-e2e-fase-8.md`](../../evidencias/execucoes/flowise-discord-e2e-fase-8.md)
- Screenshots:
  - [`docs/evidencias/screenshots/flowise-1-erro-conexao-chatflow.jpg`](../../evidencias/screenshots/flowise-1-erro-conexao-chatflow.jpg) — primeira tentativa (Chatflow + erro)
  - [`docs/evidencias/screenshots/flowise-2-agentflow-discord-ok.jpg`](../../evidencias/screenshots/flowise-2-agentflow-discord-ok.jpg) — Agentflow V2 funcionando
  - [`docs/evidencias/screenshots/discord0.jpeg`](../../evidencias/screenshots/discord0.jpeg) — alerta recebido no Discord
- Documento da fase: [`docs/prompts/desenvolvimento/fase-8-lowcode.md`](../desenvolvimento/fase-8-lowcode.md)
- Commits: `43ec8da`, `87960dc` (na `develop`)