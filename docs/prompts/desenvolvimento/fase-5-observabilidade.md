---
origem: sessão de desenvolvimento assistido (opencode)
status: oficial
data: 2026-08-29
fase: 5 — Observabilidade
---

# Fase 5 — Observabilidade

> Objetivo: produzir e correlacionar pelo menos dois sinais de observabilidade, permitindo investigar e reconstruir execuções (brief 4.6).

---

## Prompts utilizados

1. **Confirmação de sequência:**
   > "sim" — aprovação de executar a Parte 4 antes da 5 e, concluída a 4, seguir para a Parte 5 conforme plano

---

## Resultado da interação

### Sinal 1 — Logs estruturados JSON (`app/observability/logging_config.py`)
- Logger dedicado `smartorder.flow` com formatter JSON; `log_flow(request_id, node, latency_ms, **extra)` emite 1 linha por node com latência e contexto (itens, contagem, status, tipo de bloqueio)
- `setup_logging()` configura handler de console + `logs/execution.log` (gitignored); idempotente
- Cada node registra: `validate_input`, `security_check`, `get_purchase_history`, `find_similar_products`, `generate_recommendations`, `validate_recommendations`, `block_request`, `finalize_response`

### Sinal 2 — Métricas (`app/observability/metrics.py`)
- Contadores thread-safe (`threading.Lock`): runs/success/blocked/error/fallback/recomendações
- Latências: total e de tool (avg/max) + taxas (`block_rate`, `fallback_rate`)
- Endpoint **`GET /metrics`** expõe o snapshot
- `record_run` chamado no `run_recommendation` (builder) com latência total medida e soma das tools paralelas (`history_ms` + `similar_ms`)

### Terceiro sinal (da fase 4)
- Audit JSONL (`logs/audit.jsonl`) — eventos por node com `request_id`

### Insumo para a Parte 7 (anomalias)
- `settings.tool_delay_ms` (padrão 0): delay simulável dentro das tools — permite gerar anomalia de latência real e capturá-la nas métricas

### Bug de LangGraph encontrado
- Nodes retornavam `history_ms`/`similar_ms`, mas as chaves **não estavam declaradas no `RecommendationState`** → LangGraph silenciosamente as descartava (métrica de tool sempre 0). Correção: declaração no TypedDict + teste que falhava sem ela (`test_tool_delay_aparece_nas_metricas`)

### Tratamento de falhas (brief 4.6)
- LLM: timeout 30 s + max_retries 2 (config) + fallback determinístico (coocorrência) — demonstrado em execução real (`obs-real-003`)
- Tool: leitura local determinística; timeout não aplicável ao domínio (documentado); falha → erro estruturado com audit

---

## Evidências

| Evidência | Detalhe |
|---|---|
| Testes | `pytest` → **41 passed** (7 novos em `test_observability.py`: métricas de sucesso/bloqueio/erro/fallback, delay na métrica, log JSON via caplog, logs por node no grafo, endpoint `/metrics`) |
| Evidência real | 3 execuções com 3 sinais correlacionados arquivadas em [`evidencias/execucoes/observabilidade-fase-5.md`](../../evidencias/execucoes/observabilidade-fase-5.md) |
| Branch | `feature/observabilidade` |
