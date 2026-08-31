# Changelog — SmartOrder AI

> Registro do desenvolvimento por fase (Partes 0-9), estado atual e roadmap.
> Fonte viva do plano: [`docs/plano-execucao.md`](docs/plano-execucao.md) · Evidências por fase: [`docs/prompts/desenvolvimento/`](docs/prompts/desenvolvimento/README.md)

---

## ⏰ Ao retornar (31/08) — executar nesta ordem

1. **PARTE 9 (finalização, entregar até 15h):**
   - a. Consolidar prompts + refinamentos em `docs/prompts/` (critério 15)
   - b. README final (checklist 5.2) + link do vídeo
   - c. Gravar vídeo ≤12min (roteiro 5.5) → YouTube não listado → AVA
   - d. Merge `develop` → `main` + convidar professor + submeter no AVA
2. **NÃO ESQUECER (segurança):** revogar/rotacionar **após** a entrega:
   - **API key OpenCode** (exposta no chat — `LLM_API_KEY`)
   - **API key do Flowise** (se gerada — endpoint deste projeto respondeu 200 sem auth; var vazia no `.env`)
   - **Webhook do Discord** (a URL circulou no chat)
   - secret `LLM_API_KEY` no GitHub Actions (opcional, para smoke no CI) · Kanban em dia

---

## 📍 Onde paramos (31/08 — Parte 8 concluída, Parte 9 aberta)

- ✅ **Parte 8 concluída**: Agentflow V2 no Flowise Cloud montado com `poolside/laguna-s-2.1` (OpenRouter free) — request_id `3bfceacea49f` na demo E2E real (10,1 s, Discord HTTP 204)
- ✅ Evidência + 2 screenshots + JSON do agentflow versionados
- ✅ `fase-8-lowcode.md` + plano-execucao (Parte 8 ✅, critério 14 ✅) + docs atualizados
- ▶️ **Foco agora**: Parte 9 — finalizar README, vídeo ≤12min, merge `develop→main`, AVA até **15h**

---

## [0.8.0] — Parte 8: Flowise Low-Code — ✅

### Feito
- **App-side** (mergeada em `0dc052c`): `app/integrations/flowise.py` com `notify_flowise()` via httpx — chamada **best-effort** (timeout `flowise_timeout_s`, exceção engolida, resposta da API preservada), ativada por `FLOWISE_ALERTS_ENABLED=true`
- Eventos emitidos em `run_recommendation`: `security_blocked` (risco `high` p/ injection, `medium` p/ autonomia) e `recommendation_generation_failed` (fallback do LLM)
- 5 testes novos com HTTP mockado (`tests/test_flowise.py`) — habilitação, payload, erro engolido, auth opcional
- **Fluxo low-code (Agentflow V2)** no Flowise Cloud: `Start → LLM (poolside/laguna-s-2.1 via OpenRouter, temp 0,2) → Custom Function` (axios → webhook Discord); prompt SRE no System Message; webhook em variável `DISCORD_WEBHOOK_URL` (Dashboard → Variables, **não** via node Set Variable)
- Export JSON **sem segredos** versionado em [`docs/lowcode/flowise-flow.json`](docs/lowcode/flowise-flow.json) (3 nodes, 2 edges; grep `discord.com/api/webhooks/[0-9]`, `sk-or`, `Bearer`: 0 matches)
- **Demo E2E real** (request_id `3bfceacea49f`): injection → `security_check` (0,1 ms) → `flowise_notify` (6,7 s, Flowise HTTP 200) → Agentflow classifica `SEVERIDADE: alta / CAUSA PROVÁVEL: ... / AÇÃO RECOMENDADA: ...` → Discord HTTP 204. Total 10,1 s · três sinais correlacionados (logs/audit/metrics)
- Documentação: passo 2 de [`docs/lowcode/reproducao-flowise.md`](docs/lowcode/reproducao-flowise.md) reescrito com roteiro item-a-item (usuário não conhecia Flowise); evidência em [`docs/evidencias/execucoes/flowise-discord-e2e-fase-8.md`](docs/evidencias/execucoes/flowise-discord-e2e-fase-8.md); screenshots em `docs/evidencias/screenshots/`
- Decisões: N8N trial expirou → **Flowise** (aprovação do professor) → **OpenRouter** (sem integração OpenCode no Flowise Cloud) → **Agentflow V2** (Custom JS Function de Chatflow não aceita Chat Model — erro de JSON ao conectar)
- `fase-8-lowcode.md` criado com prompts, resultado, lições e evidências

---

## [0.7.0] — Parte 7: DevOps Inteligente — ✅ (`0f4fb80`)

- CI GitHub Actions: Install → ruff → pytest+cobertura → wheel (+upload de artefato); `LLM_API_KEY` via Secret (smoke test pula sem key)
- Pipeline local 3/3 verdes; **IA analisou logs dos 3 estágios** (`evidencias/pipeline/`)
- **Anomalia real**: série de 8 runs, degradação linear da tool (+300ms/run) detectada na run 5 — `evidencias/anomalias/`
- **Estimativa de tendência/risco**: regressão +178,8ms/run (global) / +300,2ms/run (conservador) → **risco ALTO: SLA 2s violado em ~3 runs** — `evidencias/metricas/`

## [0.6.0] — Parte 6: QA Inteligente — ✅ (`f5e9001`)

- **Code review com IA de diff real** (`07fbd7f`): 4 achados honestos → **A1 corrigido** (falhas de invocação agora contam nas métricas) + teste de regressão
- Cobertura **95%** (42 passed) — `docs/qa/relatorios/`
- **Priorização por risco**: matriz de 6 cenários; prioridade 1 = acesso indevido a dados de outros clientes (`llm.calls == 0` nas asserções) — `docs/qa/priorizacao-risco.md`
- Tipos de teste: unitários + integração (HTTP→grafo→tools→xlsx) + E2E real

## [0.5.0] — Parte 5: Observabilidade — ✅ (`448e233`)

- **Sinal 1**: logs JSON por node (`logs/execution.log`) com latência e contexto
- **Sinal 2**: métricas thread-safe + endpoint `GET /metrics` (contadores, latências avg/max, block_rate, fallback_rate)
- **Sinal 3**: audit JSONL (`logs/audit.jsonl`) — todos correlacionados por `request_id`
- Investigação documentada: gargalo = LLM (98,8% da latência) — `evidencias/execucoes/observabilidade-fase-5.md`
- `tool_delay_ms` simulável (insumo das anomalias da Parte 7)

## [0.4.0] — Parte 4: Segurança e Governança — ✅ (`2c3396d`)

- `app/security/guard.py`: injection (21 padrões) + ações destrutivas (15 padrões), normalização de acentos/caixa
- `app/security/audit.py`: audit JSONL correlacionado por `request_id`
- **Cenário adversarial real**: 2 ataques via HTTP bloqueados sem acionar o LLM — `evidencias/seguranca/adversarial-fase-4.md`
- Agente somente-leitura (limite de autonomia) · **Refinamento 2**: correlação do audit (checkpointer acumulava eventos → filtro por request_id)

## [0.3.0] — Parte 3: API FastAPI + Memória — ✅ (`24ff625`)

- `POST /recomendacoes` (contrato Pydantic completo: status, perfil, recomendações, `previous_recommendations`, `reason`)
- **Memória**: `MemorySaver` com thread por cliente — 2ª chamada retorna recomendações anteriores (testado)
- `request_id` UUID por execução · DI do LLM (`Depends`) — testes sem rede/custo
- Smoke real: uvicorn + curl → 200 com JSON completo — `evidencias/execucoes/api-668b104164e6-fase-3.md`

## [0.2.0] — Parte 2: Núcleo LangGraph — ✅ (`b76db1d`)

- State tipado com reducers (`operator.add`) · 8 nodes · fan-out/fan-in paralelo · edges condicionais · **DAG sem ciclos** (parada estrutural)
- `SYSTEM_PROMPT` (6 regras incl. defesa injection + autonomia) documentado — `docs/prompts/system.md`
- Fallback determinístico por coocorrência quando o LLM falha
- E2E real: `hy3-free` reproduziu o padrão semântico da base (ar-cond. → suporte) — `evidencias/execucoes/e2e-real-001-fase-2.md`
- 3 bugs corrigidos: coocorrência market-basket, tipagem `RunnableConfig`, max_tokens de reasoning → **Refinamento 1**

## [0.1.0] — Parte 1: Dados + Tools — ✅ (`a999dbc`)

- xlsx 100% confirmado (aba `PEDIDOS`, VALOR = total da linha, zero nulos) — `estrutura_planilha.md` atualizado
- `get_customer_orders` + `find_similar_products` (coocorrência) com validação Pydantic e erros claros
- 9 testes unitários (correção posterior da lógica market-basket registrada na fase 2)

## [0.0.1] — Parte 0: Fundação — ✅ (`58d76b5`→)

- Branch `develop`, `.gitignore` (`.env` protegido antes de tudo), scaffold `app/`+`tests/`, `pyproject.toml`
- LLM configurado por env: gateway OpenCode, **`hy3-free`** (conta sem saldo → modelos gratuitos testados)
- Processo permanente: **prompts de cada fase versionados antes da próxima** — `docs/prompts/desenvolvimento/`

---

## 🗺️ Roadmap restante

### Parte 9 — Finalização (31/08 até 15h)
- [ ] Consolidar prompts + refinamentos em `docs/prompts/` (critério 15)
- [ ] README final — checklist completo da seção 5.2 do brief
- [ ] **Vídeo ≤12min** (roteiro 5.5) → YouTube não listado → link no README
- [ ] Atualizar Kanban (cards 8 e 9)
- [ ] **Merge `develop` → `main`** (código final funcional na main)
- [ ] Submissão no AVA: repo + quadro + vídeo
- [ ] Convidar professor como colaborador (se ainda não feito)
- [ ] Configurar secret `LLM_API_KEY` no GitHub Actions (opcional, para smoke no CI)

### Pós-entrega (obrigatório — segurança)
- [ ] **Revogar/trocar a API key OpenCode** (`LLM_API_KEY`, exposta na conversa)
- [ ] **Rotacionar o webhook do Discord** (URL circulou no chat)
- [ ] **Rotacionar/limpar API key do Flowise** (se foi gerada; este projeto não usou — var vazia no `.env`)

---

## [0.8.1] — 31/08 — Recomendação por carrinho/produto semente (Parte 9, extra)

### Adicionado
- **API**: campo opcional `seed_products: list[int]` em `RecommendationRequest` (máx. 10) — códigos de produtos pesquisados ou no carrinho
- **Tool** `find_similar_products(..., seed_products=None)`: com sementes, a coocorrência market-basket passa a usar como base os pedidos que contêm os produtos do carrinho (excluindo os próprios sementes); sem sementes → comportamento atual intacto (zero regressão)
- **State**: `seed_products: list[int]` (state tipado)
- **Grafo**:
  - `validate_input`: filtra códigos fora do catálogo (aviso em `errors`); todos inválidos → `status: error`
  - `find_similar_products_node`: repassa `seed_products` à tool
  - `generate_recommendations` + `build_user_prompt`: seção "PRODUTOS NO CARRINHO" injetada quando há sementes
- **Teste visual sem dependência extra**: `http://localhost:8000/docs` (Swagger UI do FastAPI) — `Try it out` em `POST /recomendacoes` aceita `seed_products` e mostra o JSON
- **Classe de testes** `tests/test_carrinho.py` (11 testes): tool (coocorrência do carrinho + semente inválida + compat sem sementes), grafo (prompt contém seção + fallback usa carrinho + códigos inválidos filtrados + todos inválidos = error), API (sucesso + backward-compat + 422 para >10 + injection ainda bloqueada)

### Bugs corrigidos durante a feature
- **Erros sobrescritos entre nodes**: `generate_recommendations` zerava `errors` no caminho de sucesso → avisos do filtro de sementes eram apagados. Fix: ler `state["errors"]` no início e preservar
- **Erros vazando entre chamadas no mesmo thread** (MemorySaver): `validate_input` herdava `errors` do checkpoint anterior. Fix: `validate_input` agora começa com `errors = []` para cada nova execução

### Métricas
- Ruff limpo · **57 testes passados** (46 anteriores + 11 novos) · 1 falha pré-existente em `test_llm_smoke` (gateway não suporta mais `hy3-free`)
- 100 % backward-compatible: requisições sem `seed_products` seguem idênticas

---

## 🧭 Decisões registradas

| Decisão | Motivo |
|---|---|
| LLM `hy3-free` (gateway OpenCode) | Conta sem saldo para modelos pagos; gratuito e funcional (troca por env a qualquer momento) |
| Flowise no lugar do N8N | Trial N8N expirou; professor aprovou; melhor fit com "construção visual de agentes" (critério 14) |
| Agentflow V2 via OpenRouter | Flowise Cloud sem integração com o gateway OpenCode → modelo free equivalente via OpenRouter; Custom JS Function de chatflow não aceita Chat Model → Agentflow V2 (editor visual de agentes, mesma Prediction API; a app segue no `hy3-free`) |
| Atividade individual | Definido pelo brief (Planejamento.md corrigido) |
| Memória: MemorySaver + histórico via tool | Adequado ao domínio (base pequena, consulta por cliente); RAG vetorial desnecessário agora |
| Fallback determinístico (coocorrência) | Modelo gratuito com reasoning falha em ~1/3 das vezes — robustez + critério 15 |
| Prompts por fase versionados | Comprovação do desenvolvimento assistido por IA (critérios 12/15) |
| Recomendação por `seed_products` (carrinho) | Caso de uso "você também pode precisar" no carrinho de compras (não previsto no brief original, adicionado na Parte 9 como feature extra); backward-compatible (default = comportamento histórico) |
