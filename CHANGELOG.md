# Changelog — SmartOrder AI

> Registro do desenvolvimento por fase (Partes 0-9), estado atual e roadmap.
> Fonte viva do plano: [`docs/plano-execucao.md`](docs/plano-execucao.md) · Evidências por fase: [`docs/prompts/desenvolvimento/`](docs/prompts/desenvolvimento/README.md)

---

## 📦 Estado de Entrega (31/08)

> Snapshot vivo do que está pronto para a entrega acadêmica (15h) e o que falta fazer.

### ✅ Pronto — já no `origin/develop` (commit `2b24511` mais o roteiro `00be4b3`)

**Partes 0–8** (todas concluídas, commitadas e pushadas na `develop`):

- [x] **Parte 0** — Fundação (`58d76b5`) · scaffold, `.gitignore`, LLM por env
- [x] **Parte 1** — Dados + Tools (`a999dbc`) · `get_customer_orders` + coocorrência
- [x] **Parte 2** — Núcleo LangGraph (`b76db1d`) · 8 nodes, paralelização, DAG
- [x] **Parte 3** — API + Memória (`24ff625`) · FastAPI + `MemorySaver`
- [x] **Parte 4** — Segurança (`2c3396d`) · injection + autonomia + audit JSONL
- [x] **Parte 5** — Observabilidade (`448e233`) · logs + `/metrics` + audit correlacionado
- [x] **Parte 6** — QA com IA (`f5e9001`) · code review + cobertura 95% + matriz de risco
- [x] **Parte 7** — DevOps (`0f4fb80`) · CI 3/3 + anomalia + risco ALTO (SLA 2s)
- [x] **Parte 8** — Flowise Low-Code (`0dc052c` app + `87960dc` evidence) · Agentflow V2 → Discord (request_id `3bfceacea49f`, HTTP 204)

**Parte 9 — já prontos (esperando apenas o link do vídeo):**

- [x] README final (checklist 5.2 do brief) — commit `f134187`
- [x] Refinamento 3 (Chatflow → Agentflow V2) — commit `c258120` (critério 15)
- [x] Feature extra: **recomendação por carrinho** (`seed_products`) — commit `2b24511` (11 testes novos, 57 passed, 0 regressões)
- [x] Roteiro detalhado do vídeo de demonstração — commit `00be4b3` ([`docs/video/roteiro-video-fase-9.md`](docs/video/roteiro-video-fase-9.md))
- [x] Critérios do brief atendidos — 15/15 (rastreabilidade em [`docs/plano-execucao.md`](docs/plano-execucao.md) § 3)
- [x] Segurança: `.env` gitignored · credencial **nunca** commitada (validado por grep nos 3 commits da Parte 8/9)

**Qualidade atual:**
- Ruff limpo
- **57 testes passados** (46 anteriores + 11 do carrinho)
- 1 falha pré-existente em `test_llm_smoke` (gateway OpenCode não suporta mais `hy3-free` — fora do escopo deste commit; documentado)
- Branch `develop` 6 commits à frente da `main`; `main` intacta (1 commit original `0cabd3c`)

### ⬜ Falta para fechar a entrega — ordem sugerida

1. [ ] **Gravar o vídeo** ≤ 12 min seguindo [`docs/video/roteiro-video-fase-9.md`](docs/video/roteiro-video-fase-9.md)
   - [ ] Upload no YouTube como **não listado**
   - [ ] Copiar o link e atualizar `README.md` seção 13 (substituir o placeholder 🚧 pelo link)
2. [ ] **Commit do link** `docs: adiciona link do vídeo de demonstração` → push na `develop`
3. [ ] **Merge** `develop` → `main` (PR pode ser local — `git checkout main && git merge --no-ff develop`)
4. [ ] **Convidar o professor como colaborador** no GitHub (Settings → Collaborators)
5. [ ] **Submeter no AVA** (Projeto Avaliativo – M2.2):
   - Link do repositório (`https://github.com/gisele-coder/SmartAgenteVendas`)
   - Link do quadro Kanban
   - Link do vídeo (YouTube não listado)
6. [ ] **Atualizar o Kanban** (mover cards 8 e 9 para "Concluído")
7. [ ] **Não alterar o repositório após 15h** (regra do brief § 7)

### 🛑 Pós-entrega — segurança (obrigatório)

- [ ] **Revogar/rotacionar a API key OpenCode** (`LLM_API_KEY`, exposta no chat)
- [ ] **Rotacionar o webhook do Discord** (a URL circulou no chat)
- [ ] **Rotacionar/limpar a API key do Flowise** (este projeto não usou — var vazia no `.env`, mas vale verificar no Dashboard → API Keys)

### 📊 Resumo de critérios do brief

| Critério | Status | Artefato |
|---|---|---|
| 1 — Vídeo ≤12 min, YouTube não listado | ⬜ pendente | roteiro pronto; gravar e subir |
| 2 — Cards no quadro com descrições | ✅ | Kanban |
| 3 — Quadro atualizado durante o desenvolvimento | ✅ | histórico |
| 4 — Branches, commits semânticos, develop→feature→main | ✅ | 9+ feature branches; commits descritivos |
| 5 — README completo e reproduzível | ✅ | `README.md` (seção 5.2) |
| 6 — App funcional, 2 cenários, saída estruturada | ✅ | API + JSON Pydantic |
| 7 — LangGraph: state, nodes, sequencial+condicional+paralelo, parada | ✅ | `app/graph/` 8 nodes, DAG |
| 8 — Tool integrada com validação e tratamento de falhas | ✅ | `app/tools/` |
| 9 — Memória/contexto adequada | ✅ | `MemorySaver` + histórico via tool |
| 10 — Segurança, autonomia, cenário adversarial | ✅ | `app/security/` + evidência |
| 11 — 2 sinais de observabilidade + timeout/retry/fallback | ✅ | logs + `/metrics` + audit JSONL |
| 12 — IA em code review + testes (integração/aceitação/E2E) + risco | ✅ | `docs/qa/` |
| 13 — Pipeline + IA + anomalia + estimativa de risco | ✅ | CI + evidências + projeção |
| 14 — Low-code integrado com trigger e saída observável | ✅ | Flowise Agentflow V2 + Discord |
| 15 — Refinamento documentado (problema→alteração→resultado) | ✅ | 3 ciclos em `docs/prompts/refinamentos/` |

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

## 🗺️ Próximos passos (resumo)

> Ver a seção **📦 Estado de Entrega** acima para o checklist detalhado (do ✅ pronto ao ⬜ pendente).

**Curto prazo (antes das 15h):** gravar o vídeo a partir do roteiro pronto → atualizar README com o link → commit → merge `develop → main` → AVA.

**Pós-entrega:** revogar `LLM_API_KEY`, rotacionar o webhook do Discord e (se houver) a API key do Flowise.

---

## [0.9.0] — 31/08 — Finalização / Entrega (Parte 9) — ⏳ em curso

### Feito
- **README final** (commit `f134187`) — atende integralmente a seção 5.2 do brief: descrição/classificação/arquitetura, tool, memória, segurança, 7 cenários (incluindo carrinho), QA/observabilidade/DevOps, low-code Flowise, instalação, testes, 3 refinamentos linkados + limitações, links para toda a documentação, placeholder do vídeo
- **Refinamento 3** (commit `c258120`) — Chatflow → Agentflow V2 (erro de JSON ao conectar) documentado em [`docs/prompts/refinamentos/refinamento-3-chatflow-para-agentflow-v2.md`](docs/prompts/refinamentos/refinamento-3-chatflow-para-agentflow-v2.md) — atende critério 15
- **Feature extra: recomendação por carrinho** (commit `2b24511`) — `seed_products: list[int]` no request, coocorrência market-basket com base no carrinho, 11 testes novos, 0 regressões
- **Roteiro detalhado do vídeo** (commit `00be4b3`) — [`docs/video/roteiro-video-fase-9.md`](docs/video/roteiro-video-fase-9.md) com timestamps, falas, comandos `curl` prontos e checklist pré-gravação
- Documentação consolidada: README, CHANGELOG, plano-execucao, prompts (9 fases + 3 refinamentos) — todos sincronizados

### Pendente (ordem)
- [ ] Gravar vídeo (≤ 12 min) seguindo o roteiro
- [ ] Upload no YouTube como não listado
- [ ] Substituir o placeholder 🚧 na seção 13 do README pelo link
- [ ] Commit do link + push na `develop`
- [ ] **Merge `develop` → `main`** (manter `main` como versão final funcional)
- [ ] Convidar professor como colaborador
- [ ] Submeter links (repo + quadro + vídeo) no AVA — **antes das 15h**
- [ ] Atualizar Kanban (cards 8 e 9 → Concluído)
- [ ] Não alterar o repositório após o prazo (brief § 7)

### Pós-entrega (segurança)
- [ ] Revogar `LLM_API_KEY` OpenCode (exposta no chat)
- [ ] Rotacionar webhook do Discord
- [ ] Rotacionar/limpar API key do Flowise (se gerada)

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
