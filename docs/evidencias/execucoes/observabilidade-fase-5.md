# Execução — Observabilidade (Fase 5)

**Data:** 2026-08-29 · **Fase:** 5 — Observabilidade · **Tipo:** 3 execuções reais com captura dos sinais correlacionados por `request_id`

---

## Sinais da aplicação

| Sinal | Meio | Correlação |
|---|---|---|
| **1. Logs estruturados JSON** | `logs/execution.log` (logger `smartorder.flow`, 1 linha JSON por node com latência) | `request_id` |
| **2. Métricas agregadas** | `GET /metrics` (contadores, latências, taxas) | agregado por execução gravada |
| **3. Audit log JSONL** | `logs/audit.jsonl` (eventos por node) | `request_id` |

## Execuções

1. **`obs-real-001`** — fluxo principal com LLM real (`hy3-free`): success, 3 recomendações, LLM = 22.921,5 ms
2. **`obs-real-002`** — prompt injection: blocked em <1 ms (caminho curto: validate → security → block → finalize, sem tools/LLM)
3. **`obs-real-003`** — pico de latência simulado na tool (`tool_delay_ms=500`): tools = 503,0/507,9 ms; LLM falhou em produzir JSON → **fallback determinístico acionado** (`fallback_rate` 0,33)

## Snapshot `GET /metrics` após as 3 execuções

```json
{
 "runs_total": 3,
 "success_total": 2,
 "blocked_total": 1,
 "error_total": 0,
 "fallback_total": 1,
 "recommendations_total": 3,
 "total_ms_max": 29203.3,
 "tool_ms_max": 1010.9,
 "total_ms_avg": 17462.8,
 "tool_ms_avg": 344.7,
 "block_rate": 0.33,
 "fallback_rate": 0.33
}
```

## Logs estruturados (amostra — `logs/execution.log`)

```json
{"request_id": "obs-real-001", "node": "get_purchase_history", "latency_ms": 2.6, "items": 30, "orders": 10}
{"request_id": "obs-real-001", "node": "generate_recommendations", "latency_ms": 22921.5, "source": "llm", "count": 3}
{"request_id": "obs-real-002", "node": "security_check", "latency_ms": 0.1, "blocked": true, "kind": "injection"}
{"request_id": "obs-real-003", "node": "get_purchase_history", "latency_ms": 503.0, "items": 32, "orders": 11}
{"request_id": "obs-real-003", "node": "generate_recommendations", "latency_ms": 28688.9, "source": "fallback", "error": "resposta do LLM sem array JSON"}
```

## Investigação da execução `obs-real-001` (requisito do brief 4.6)

- **Fluxo percorrido**: validate_input → security_check → [get_purchase_history ∥ find_similar_products] → generate_recommendations → validate_recommendations → finalize_response
- **Decisões relevantes**: security_ok (consulta legítima); LLM escolheu 3 produtos do catálogo com justificativas; validação determinística manteve os 3 (todos no catálogo)
- **Erros**: nenhum; **latência**: gargalo absoluto no LLM (22,9 s de 23,2 s totais — 98,8%)

## Conclusão da análise

- Correlação 1:1 entre os três sinais via `request_id` permite reconstruir qualquer execução
- O gargalo é o LLM (modelo gratuito com reasoning) — metrics e logs deixam isso evidente; justifica o fallback e alimenta a análise de anomalias da Parte 7
- O pico simulado de tool latency (500 ms → capturado como ~1010 ms somando as duas tools paralelas) demonstra que a métrica detecta anomalias reais
