# Changelog — SmartOrder AI

> Registro do desenvolvimento por fase (Partes 0-9), estado atual e roadmap.
> Fonte viva do plano: [`docs/plano-execucao.md`](docs/plano-execucao.md) · Evidências por fase: [`docs/prompts/desenvolvimento/`](docs/prompts/desenvolvimento/README.md)

---

## ⏰ Ao retornar (30/08) — executar nesta ordem

1. **PARTE 8 (fechar):**
   - a. Discord webhook (2 min) → [`docs/lowcode/reproducao-flowise.md`](docs/lowcode/reproducao-flowise.md) passo 1
   - b. Chatflow no Flowise Cloud (10 min) → passos 2.1–2.6 do mesmo doc
   - c. Exportar o chatflow como `docs/lowcode/flowise-flow.json`
   - d. Passar para o assistente: `FLOWISE_URL`, `FLOWISE_API_KEY`, `FLOWISE_CHATFLOW_ID` → `.env` + **demo end-to-end real** (injection → Discord) → evidência arquivada
   - e. `fase-8-lowcode.md` + Parte 8 ✅ no plano-execucao + critério 14 + Kanban
2. **PARTE 9 (finalização, entregar até 15h):**
   - a. Prompts consolidados + refinamento (critério 15)
   - b. README final (checklist 5.2) + link do vídeo
   - c. Gravar vídeo ≤12min (roteiro 5.5) → YouTube não listado → AVA
   - d. Merge `develop` → `main` + convidar professor + submeter no AVA
3. **NÃO ESQUECER:** revogar a API key OpenCode **após** a entrega (exposta no chat) · secret `LLM_API_KEY` no Actions (opcional) · Kanban em dia

---

## 📍 Onde paramos (29/08 — fim da Parte 8, lado da aplicação)

- ✅ **Parte 8 (app-side) mergeada** — `0dc052c` · **47 passed** · Ruff limpo
- ✅ Integração Flowise pronta e testada (best-effort, env-gated, não quebra a API)
- ⏸️ **BLOQUEIO — aguardando ação do usuário** (fluxo visual no Flowise + Discord, roteiro pronto em [`docs/lowcode/reproducao-flowise.md`](docs/lowcode/reproducao-flowise.md))

---

## [0.8.0] — Parte 8: Flowise Low-Code — **EM ANDAMENTO**

### Feito
- `app/integrations/flowise.py`: `notify_flowise()` via httpx — timeout 5s, chamada best-effort (exceção engolida, resposta da API preservada), ativado por `FLOWISE_ALERTS_ENABLED=true`
- Emissão de eventos em `run_recommendation`: `security_blocked` (risco `high` p/ injection, `medium` p/ autonomia) e `recommendation_generation_failed` (fallback do LLM)
- 5 testes novos com HTTP mockado (habilitado/desabilitado/erro engolido/payload correto)
- Passo a passo completo de reprodução: `docs/lowcode/reproducao-flowise.md`
- Decisão registrada: N8N trial expirou → **Flowise** (aprovação do professor; melhor fit com "construção visual de agentes")

### Falta para concluir a Parte 8 (ação do usuário)
- [ ] Criar webhook do Discord (servidor → canal → Integrações → Webhooks)
- [ ] Montar o Chatflow no Flowise Cloud (ChatOpenAI Custom `hy3-free` + prompt SRE + Custom Function → Discord) — roteiro exato no doc
- [ ] Exportar o chatflow como `docs/lowcode/flowise-flow.json` (versionar)
- [ ] Passar URL/API key/Chatflow ID → configurar `.env` local
- [ ] Evidência end-to-end real (injection → alerta no Discord) arquivada em `docs/evidencias/`
- [ ] `fase-8-lowcode.md` + Parte 8 ✅ no plano-execucao + critério 14 marcado

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

### Concluir Parte 8 (ver pendências acima — usuário + evidência)

### Parte 9 — Finalização (31/08 até 15h)
- [ ] Consolidar prompts + refinamentos em `docs/prompts/` (critério 15)
- [ ] README final — checklist completo da seção 5.2 do brief
- [ ] **Vídeo ≤12min** (roteiro 5.5) → YouTube não listado → link no README
- [ ] Atualizar Kanban (cards 8 e 9)
- [ ] **Merge `develop` → `main`** (código final funcional na main)
- [ ] Submissão no AVA: repo + quadro + vídeo
- [ ] Convidar professor como colaborador (se ainda não feito)
- [ ] Configurar secret `LLM_API_KEY` no GitHub Actions (opcional, para smoke no CI)

### Pós-entrega (obrigatório)
- [ ] **Revogar/trocar a API key OpenCode** (exposta na conversa) — critério 10

---

## 🧭 Decisões registradas

| Decisão | Motivo |
|---|---|
| LLM `hy3-free` (gateway OpenCode) | Conta sem saldo para modelos pagos; gratuito e funcional (troca por env a qualquer momento) |
| Flowise no lugar do N8N | Trial N8N expirou; professor aprovou; melhor fit com "construção visual de agentes" (critério 14) |
| Atividade individual | Definido pelo brief (Planejamento.md corrigido) |
| Memória: MemorySaver + histórico via tool | Adequado ao domínio (base pequena, consulta por cliente); RAG vetorial desnecessário agora |
| Fallback determinístico (coocorrência) | Modelo gratuito com reasoning falha em ~1/3 das vezes — robustez + critério 15 |
| Prompts por fase versionados | Comprovação do desenvolvimento assistido por IA (critérios 12/15) |
