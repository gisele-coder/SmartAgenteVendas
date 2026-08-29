---
origem: sessão de planejamento do projeto (opencode)
status: oficial
data: 2026-08-29
finalidade: documento-mestre de execução — partes 0-9, critérios atendidos, evidências e observações de entrega
relacionado: [./README.md](./README.md) | [./prompts/desenvolvimento/](./prompts/desenvolvimento/README.md)
---

# Plano de Execução — SmartOrder AI

> **Documento-mestre**: mapa de todas as partes do projeto (0-9), sua relação com os critérios do brief, status, evidências e observações. Atualizado ao fim de cada parte para não perder o fio da entrega.

---

## 1. Visão Geral

| Item | Definição |
|---|---|
| Projeto | **SmartOrder AI** — Agente Inteligente de Pedidos e Recomendações |
| Problema | Empresas com histórico de pedidos demoram a identificar padrões e oportunidades de recomendação |
| Entrada | `customer_id` (e requisição em linguagem natural) |
| Saída | JSON estruturado: perfil do cliente + recomendações justificadas + status |
| Modalidade | **Individual** (brief seção 3) |
| Formato | API local (FastAPI) |
| Stack | Python 3.11+ · LangGraph · FastAPI · Pydantic v2 · pandas+openpyxl · pytest · ruff · GitHub Actions · Flowise Cloud (low-code) |
| LLM | Gateway OpenCode (`https://opencode.ai/zen/v1`), modelo **`hy3-free`** (conta sem saldo; planos B: `nemotron-3.5-lightning-free`) — config 100% por env |
| Base de dados | `data/base_ficticia_pedidos_agente_ia.xlsx` — 343 itens, 120 pedidos, 12 clientes, 22 produtos (estrutura 100% confirmada) |
| Entrega | **31/08/26 às 15h** (submissão no AVA: repo + quadro + vídeo) |
| Domínio real futuro | Trocar a fonte xlsx pelo WebService do ERP do cliente sem alterar a lógica do agente |

---

## 2. Tabela Mestra — Partes 0 a 9

| # | Parte | Escopo / Entregáveis | Critérios brief | Status | Evidências | Observações |
|---|---|---|---|---|---|---|
| 0 | **Fundação** | Branch `develop`, `.gitignore`, scaffold (`app/`, `tests/`), `pyproject.toml`, `.env.example`, config LLM validada, registro de prompts por fase | 3, 2 | ✅ **Concluída** | commits `191733c`, `ee97ca9`, `58d76b5` · pytest 2 passed · ruff ok | Conta OpenCode sem saldo → modelo gratuito `hy3-free` testado e fixado; key só no `.env` |
| 1 | **Dados + Tools** | Inspecionar xlsx, `get_customer_orders` + `find_similar_products` (coocorrência), schemas Pydantic, erros claros | 8 | ✅ **Concluída** | commits `af31cdc`, `030bc24`, `641474a`, merge `a999dbc` · pytest 11 passed | Aba real `PEDIDOS`; `VALOR` = total da linha; zero nulos; `estrutura_planilha.md` atualizado com `## Correções` |
| 2 | **Núcleo LangGraph** | State tipado, 8 nodes (`validate_input`, `security_check`, `block_request`, `get_purchase_history` ∥ `find_similar_products`, `generate_recommendations`, `validate_recommendations`, `finalize_response`), edges condicionais, paralelização, condição de parada, separação LLM × regras | 6, 7 | ✅ **Concluída** | pytest 17 passed · E2E real `hy3-free` · branch `feature/langgraph-core` | 3 bugs corrigidos (coocorrência market-basket, injeção de config, max_tokens de reasoning) → Refinamento 1 documentado; DAG sem ciclos = parada estrutural |
| 3 | **API + Memória** | `POST /recomendacoes`, `request_id` por execução, `MemorySaver` (checkpointer), perfil do cliente no State | 5, 9 | ✅ **Concluída** | pytest 24 passed · smoke real uvicorn+curl (`api-668b104164e6`) · branch `feature/api-memoria` | Memória por thread de cliente (`previous_recommendations`); DI do LLM para testes sem rede |
| 4 | **Segurança** | Módulo `app/security/` (guard: injection + ações destrutivas com normalização; audit JSONL), bloqueio pré-LLM, agente somente-leitura, cenário adversarial real | 10 | ✅ **Concluída** | pytest 34 passed · evidência `adversarial-fase-4.md` (2 ataques bloqueados via HTTP) · branch `feature/governanca` | Bug de correlação do audit descoberto pela evidência → Refinamento 2 |
| 5 | **Observabilidade** | Logs JSON por node (`logs/execution.log`), métricas agregadas + `GET /metrics`, audit JSONL correlacionado por `request_id`, timeout/retry no LLM, delay simulável na tool | 11 | ✅ **Concluída** | pytest 41 passed · evidência `observabilidade-fase-5.md` (3 execuções, 3 sinais correlacionados) · branch `feature/observabilidade` | Bug de chaves não declaradas no State corrigido; LLM confirmado como gargalo (98,8%) |
| 6 | **QA** | Code review com IA de diff real (commit `07fbd7f`: 4 achados, 1 correção), cobertura 95% arquivada, priorização por risco (matriz 6 cenários), testes unit+integração+E2E consolidados | 12 | ✅ **Concluída** | pytest 42 passed · `docs/qa/` populada (review + relatório + matriz) · branch `feature/qa-inteligente` | Achado A1: falhas de invocação agora contam nas métricas |
| 7 | **DevOps** | CI GitHub Actions (ruff→pytest+cobertura→wheel, secret LLM_API_KEY), IA analisa 3 estágios do pipeline, anomalia linear detectada na run 5 de série de 8, regressão + projeção de SLA | 13 | ✅ **Concluída** | pipeline 3/3 local · `evidencias/pipeline/`, `anomalias/`, `metricas/` · branch `feature/devops-anomalias` | Risco ALTO: SLA 2s violado em ~3 runs se tendência continuar |
| 8 | **Flowise Low-code** | `app/integrations/flowise.py` (webhook best-effort nos eventos `security_blocked`/`recommendation_generation_failed`) → Chatflow Flowise (ChatOpenAI Custom `hy3-free` + prompt SRE + Custom Function) → alerta no Discord + resposta registrada; export JSON do fluxo versionado | 14 | ⬜ Pendente | — | **Decisão 29/08**: N8N trial expirou; professor aprovou Flowise (construção visual de agentes). Requer: conta Flowise Cloud + webhook Discord |
| 9 | **Finalização** | `docs/prompts/system.md` + ciclo de refinamento, README completo (seção 5.2), evidências, vídeo (roteiro 5.5), merge `develop→main`, submissão AVA | 1, 4, 15 | ⬜ Pendente | — | **Revogar API key após a entrega** |

---

## 3. Rastreabilidade — 15 Critérios do Brief (seção 6)

| Critério | Descrição (resumo) | Parte | Artefato comprobatório |
|---|---|---|---|
| 1 | Vídeo ≤12min, YouTube não listado | 9 | Link no README |
| 2 | Cards no quadro com descrições claras | 0 | GitHub Project |
| 3 | Quadro atualizado durante o desenvolvimento | contínuo | Histórico de movimentação |
| 4 | Branches, commits semânticos, fluxo develop→feature→main | 0+ | Histórico do repo |
| 5 | README.md completo e reproduzível | 9 | `README.md` |
| 6 | App funcional, 2 cenários, saída estruturada | 2-5 | API + JSON Pydantic |
| 7 | LangGraph: state, nodes, sequencial+condicional+paralelo, parada | 2 | `app/graph/` ✅ |
| 8 | Tool integrada com validação e tratamento de falhas | 1 | `app/tools/` ✅ |
| 9 | Memória/contexto adequada | 3 | Checkpointer `MemorySaver` + histórico via tool ✅ |
| 10 | Segurança, autonomia, cenário adversarial | 4 | `app/security/` + evidência adversarial real ✅ |
| 11 | 2 sinais de observabilidade + timeout/retry/fallback | 5 | Logs JSON + métricas `/metrics` + audit JSONL ✅ |
| 12 | IA em code review + testes (integração/aceitação/E2E) + priorização por risco | 6 | `docs/qa/` (review, cobertura 95%, matriz de risco) ✅ |
| 13 | Pipeline + IA analisa logs + anomalia + estimativa de risco | 7 | CI yml + pipeline/evidências + regressão/projeção ✅ |
| 14 | Low-code integrado com trigger e saída observável | 8 | Fluxo Flowise (export JSON) + evidência end-to-end |
| 15 | Refinamento documentado (problema→alteração→resultado) | 9 | `docs/prompts/refinamentos/` |

---

## 4. Observações de Entrega

### Pendências do usuário (não bloqueiam o código)
- [ ] **Convidar o professor como colaborador** no repo (checklist do brief)
- [x] ~~Criar conta N8N Cloud~~ → **Decisão 29/08**: N8N Cloud expirou o trial; professor aprovou **Flowise** como alternativa (e melhor fit com o critério: construção visual de agentes). Pendências atuais: conta Flowise Cloud (free tier) + webhook Discord
- [ ] Manter o **Kanban atualizado** a cada parte (cards prontos na conversa; mover "Fluxo LangGraph" para Em Andamento agora)
- [ ] Gravar o vídeo (roteiro 5.5: 0-1 problema, 1-2 arquitetura, 2-4 cenários, 4-5 segurança, 5-6 QA, 6-8 pipeline/anomalia/risco, 8-9 low-code Flowise, 9-10 limitações)

### Riscos e mitigações
| Risco | Mitigação |
|---|---|
| Conta OpenCode sem saldo (modelos pagos bloqueados) | Uso de `hy3-free` (custo 0); troca por env; fallback determinístico por coocorrência |
| `hy3-free` é modelo de reasoning (consome tokens pensando; `content` ok) | `max_tokens` folgado (800+), temperatura 0.2, validação determinística do JSON |
| Quota/instabilidade do modelo gratuito | Retry limitado + fallback: recomendações por coocorrência pura |
| Prazo curto (2,5 dias) | Cortes permitidos: interface visual, Docker. **Nenhum critério do brief é cortável** |
| Credencial exposta = nota zero | `.env` gitignored desde o início; **revogar a key após 31/08** |

### Regras de processo permanentes
1. **Prompts por fase**: toda Parte N gera `docs/prompts/desenvolvimento/fase-N-<nome>.md` **antes** da Parte N+1
2. **Git**: `develop → feature/<tema> → develop → (final) main`, commits semânticos
3. **Testes/lint antes de commit**: `ruff check .` + `pytest` sempre verdes
4. **Kanban coerente**: cards refletem o estado real das partes (mover em Concluído com a parte)

---

## 5. Cronograma

| Dia | Partes | Resultado esperado |
|---|---|---|
| **Sáb 29/08** | 0 ✅ · 1 ✅ · 2 | Núcleo LangGraph funcionando end-to-end em modo texto |
| **Dom 30/08** | 3, 4, 5, 6, 7, 8 | API completa, segura, observável, testada, com CI e low-code (Flowise) |
| **Seg 31/08** | 9 | README final, vídeo, evidências, merge `main`, AVA até **15h** |

---

## 6. Histórico de Atualizações

| Data | Atualização |
|---|---|
| 29/08 | Criação do documento; Partes 0 e 1 concluídas com evidências |
| 29/08 | Parte 2 concluída: grafo LangGraph com paralelização e fallback validado end-to-end com o modelo real; 3 bugs corrigidos; Refinamento 1 documentado (`docs/prompts/refinamentos/`) |
| 29/08 | Revisão documental pré-Parte 3: correções posteriores registradas na fase 1, README expandido, execução real `e2e-real-001` arquivada em `docs/evidencias/execucoes/` |
| 29/08 | Parte 3 concluída: API FastAPI com contrato Pydantic, checkpointer por thread de cliente e smoke test real registrado em evidências |
| 29/08 | Parte 4 concluída: módulo de segurança (injection + ações destrutivas), audit JSONL correlacionado e cenário adversarial real com 2 ataques bloqueados; Refinamento 2 (correlação do audit) documentado |
| 29/08 | Parte 5 concluída: logs JSON por node, métricas com `/metrics` e investigação de execução documentada com 3 sinais correlacionados por `request_id` |
| 29/08 | Parte 6 concluída: code review com IA de diff real (correção aplicada), cobertura 95% e priorização de testes por risco documentadas em `docs/qa/` |
| 29/08 | Parte 7 concluída: CI configurado (ruff→pytest→wheel), IA analisa 3 estágios, anomalia linear detectada/explicada e estimativa de tendência/risco (ALTO) documentadas |
| 29/08 | Decisão de low-code: N8N Cloud expirou → **Flowise** (aprovação do professor, melhor fit com construção visual de agentes); plano da Parte 8 atualizado (Flowise Cloud + Discord + hy3-free) |
