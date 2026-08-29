# Code Review — commit `07fbd7f` (Parte 5 — Observabilidade)

**Data:** 2026-08-29 · **Revisor:** IA (análise assistida, opencode) · **Diff analisado:** `git show 07fbd7f -- app/` (builder.py, observability/, nodes.py, tools/)

## Contexto

Commit que introduziu logs JSON por node, métricas agregadas e endpoint `/metrics`. Review focado em corretude de concorrência, correlação de sinais e cobertura de caminhos de falha.

## Achados da IA

### 🔴 A1 — Falhas de invocação não registradas nas métricas (corrigido)
**Local:** `app/graph/builder.py` — `run_recommendation`
**Problema:** `record_run` só é chamado **após** `build_graph().invoke(...)` retornar. Se o invoke lançar exceção (ex.: falha na leitura da base, erro não capturado pelo fallback), a execução **nunca entra nas métricas** — um aumento real de taxa de erro ficaria invisível no `/metrics`, comprometendo a detecção de anomalias (critérios 11 e 13 do brief).
**Severidade:** média-alta · **Decisão:** ✅ **corrigido** — `try/except` envolvendo o invoke: registra `record_run("error", ...)` e relança para a API responder 500. Teste novo cobre o caminho.

### 🟡 A2 — Custo de double-parse no formatter JSON (aceito)
**Local:** `app/observability/logging_config.py` — `JsonFormatter.format`
**Problema:** cada linha de log tenta `json.loads` da mensagem antes de montar o payload — parse duplicado por linha.
**Decisão:** ⏸️ aceito — volume atual é baixo (8 linhas/execução); alternativa (payload dict como `msg`) quebraria a asserção de mensagem única nos testes. Registrado como trade-off consciente.

### 🟡 A3 — `snapshot()` com cópia rasa (aceito, com ressalva)
**Local:** `app/observability/metrics.py`
**Problema:** `dict(_metrics)` é cópia rasa — se surgirem valores aninhados no futuro, o snapshot poderia expor mutáveis internos fora do lock.
**Decisão:** ⏸️ aceito — valores atuais são escalares imutáveis; nota documentada para evolução futura.

### 🟢 A4 — Padrões corretos identificados (positivo)
- `snapshot()` copia **sob lock** e computa agregados fora dele — cópia atômica, consistente
- Chaves de métricas fixas (sem crescimento descontrolado de memória)
- `reset()` para testes isolados por fixture `autouse`

## Correção aplicada (A1)

```python
# app/graph/builder.py — run_recommendation
t0 = time.perf_counter()
try:
    result = build_graph().invoke(request, config={"configurable": configurable})
except Exception:
    total_ms = round((time.perf_counter() - t0) * 1000, 1)
    record_run("error", True, 0, total_ms, 0.0)   # marca fallback pois nenhum output foi produzido
    raise
```

```python
# tests/test_observability.py — novo teste
def test_metricas_registram_falha_de_invocacao(monkeypatch):
    def _boom():
        raise RuntimeError("falha simulada da tool")
    monkeypatch.setattr("app.graph.builder.build_graph", _boom)
    with pytest.raises(RuntimeError):
        run_recommendation({"request_id": "fail-001", "customer_id": 100011, "query": ""}, llm=FakeLLM("{}"))
    snap = snapshot()
    assert snap["runs_total"] == 1
    assert snap["error_total"] == 1
```

## Evidência

- Diff analisado: `git show 07fbd7f`
- Correção aplicada neste branch (`feature/qa-inteligente`) junto com o teste de regressão
- Cobertura pós-correção: ver [`../relatorios/relatorio-cobertura-2026-08-29.md`](../relatorios/relatorio-cobertura-2026-08-29.md)
