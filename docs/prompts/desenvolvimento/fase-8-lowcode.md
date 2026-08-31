---
origem: sessão de desenvolvimento assistido (opencode)
status: oficial
data: 2026-08-31
fase: 8 — Flowise Low-Code
---

# Fase 8 — Flowise Low-Code

> Objetivo: ferramenta low-code (Flowise Cloud) acionada por evento HTTP da aplicação, com classificação de severidade por LLM e alerta observável no Discord (critério 14). A lógica principal permanece na aplicação; o Flowise é apoio visual.

---

## Prompts utilizados

1. **Decisão de low-code (usuário, parte 1 — já documentada):** N8N trial expirou → professor aprovou Flowise
2. **Decisão de credencial/node (parte 2):** Flowise Cloud não tem integração OpenCode → credencial e node do chatflow alterados para ChatOpenRouter (modelo free via OpenRouter)
3. **Depuração do erro de conexão (parte 3):** "Quando tento conectar o output do OpenRouter com o Input do Custom JS Function dá erro de Json" — levantada via leitura do código-fonte atual do node (`packages/components/nodes/utilities/CustomFunction/CustomFunction.ts` v3.0); causa: o anchor "Input Variables" é tipado como `json`, incompatível com saída de Chat Model
4. **Diagnóstico e decisão de migração:** "Percebi que o problema estava em eu tentar configurar o Flowiseai com Chatflows e não com Agentflows V2 disponível, mais apropriado para meu caso na ferramenta. Poderia atualizar a documentação e a configuração do Flowise com o Agentflows V2?" — confirmação da solução e aprovação do roteiro
5. **Pedido de detalhamento (usuário):** "seja detalhista nos passos do flowise pois não conheço muito a ferramenta" — passo 2 de `reproducao-flowise.md` reescrito com roteiro item-a-item
6. **Coleta de artefatos (usuário):** JSON exportado do agentflow + URL + ID + confirmação visual do alerta no Discord

---

## Resultado da interação

### Aplicação (`app/integrations/flowise.py`)
- `notify_flowise()` via `httpx` — chamada **best-effort** (exceção engolida), ativada por `FLOWISE_ALERTS_ENABLED=true` (mergeada em `0dc052c`)
- Eventos emitidos em `run_recommendation`: `security_blocked` (risco `high` para injection, `medium` para autonomia) e `recommendation_generation_failed` (fallback do LLM)
- 5 testes novos (`tests/test_flowise.py`) — habilitação, payload, erro engolido, auth opcional
- Nenhuma alteração de código na Parte 8 baixa — a integração Python já estava pronta

### Fluxo no Flowise Cloud — Chatflow → Agentflow V2 (decisão chave)
- **Primeira tentativa (descartada)**: Chatflow V1 com `ChatPrompt → ChatOpenRouter → Custom Function` — **falhou**: o node *Custom JS Function* (v3.0) não aceita Chat Model (única entrada é anchor JSON), gerando o erro de JSON relatado pelo usuário
- **Solução**: reconstrução como **Agentflow V2** (`Start → LLM → Custom Function`); o V2 é o editor visual de agentes do Flowise, encadeia os três nativamente e usa o mesmo endpoint de Prediction API
- **LLM configurado**: `poolside/laguna-s-2.1` (OpenRouter free, temp 0,2) — slug completo descoberto via `responseMetadata.model_name` no trace do Flowise
- **Webhook**: variável `DISCORD_WEBHOOK_URL` em **Dashboard → Variables** (não use o node "Set Variable"), acessível via `$vars` no Custom Function
- **Custom Function**: `require('axios')` → `POST $vars.DISCORD_WEBHOOK_URL` com o alerta classificado em `content`
- **Sem segredos no JSON exportado** (validado por grep — `discord.com/api/webhooks/[0-9]`, `sk-or`, `Bearer`: nenhum match); seguro para versionar
- Exportado como `docs/lowcode/flowise-flow.json` (99,6 KB, 3 nodes, 2 edges)

### Demo end-to-end real (`request_id: 3bfceacea49f`)
- Requisição adversarial → `security_check` bloqueou (0,1 ms) → `flowise_notify` em 6,7 s → Agentflow V2 classificou (`SEVERIDADE: alta / EVENTO: ... / CAUSA PROVÁVEL / AÇÃO RECOMENDADA`) → Discord HTTP 204
- Três sinais correlacionados por `request_id`: logs JSON, audit JSONL, métricas (`/metrics`)
- Latência: 10,1 s total (98,8 % no Flowise — confirma Parte 5: LLM é o gargalo, agora em dois níveis)
- Alerta visual no canal `#smartorder-alertas` confirmado pelo usuário

### Decisões e trade-offs
- **FLOWISE_API_KEY vazio**: o endpoint `cloud.flowiseai.com/api/v1/prediction/<id>` respondeu **200 sem autenticação** (Flowise Cloud free, flow público); código já trata `flowise_api_key` opcional (`app/integrations/flowise.py:30`)
- **`flowise_timeout_s=45`** (não 5): modelo free de reasoning pode levar 5–10 s; timeout alto evita alarmes falsos sem bloquear a API (chamada é best-effort)
- **Webhook do Discord em variável do Flowise**: chave não trafega no `.env` da aplicação nem em logs

---

## Correção documental

- **30/08**: Flowise Cloud sem integração OpenCode → credencial/node `ChatOpenRouter`
- **31/08** (esta fase): Custom JS Function de Chatflow v3.x rejeita Chat Model → fluxo reconstruído como **Agentflow V2**; passo 2 de `reproducao-flowise.md` reescrito com roteiro detalhado (usuário não conhecia a ferramenta); `reproducao-flowise.md` passo 3 atualizado com `.env` real deste projeto; novo registro "Atualizar pendência pós-entrega: rotacionar URL do webhook Discord e API key do Flowise"

---

## Evidências

| Evidência | Detalhe |
|---|---|
| Demo E2E | [`evidencias/execucoes/flowise-discord-e2e-fase-8.md`](../../evidencias/execucoes/flowise-discord-e2e-fase-8.md) — request_id `3bfceacea49f`, todos os sinais correlacionados, alerta confirmado no Discord |
| Fluxo versionado | [`docs/lowcode/flowise-flow.json`](../../lowcode/flowise-flow.json) — 3 nodes, 2 edges, sem segredos |
| Screenshots | [`evidencias/screenshots/flowise-1-erro-conexao-chatflow.jpg`](../../evidencias/screenshots/flowise-1-erro-conexao-chatflow.jpg) (erro do Chatflow) · [`evidencias/screenshots/flowise-2-agentflow-discord-ok.jpg`](../../evidencias/screenshots/flowise-2-agentflow-discord-ok.jpg) (Agentflow V2 funcionando) |
| Critério 14 | Atendido: ferramenta low-code com trigger (HTTP da app) e saída observável (mensagem Discord) |