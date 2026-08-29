# Refinamento 2 — Contaminação de correlação no audit log

**Data:** 2026-08-29 · **Fase:** 4 (Segurança e Governança)

## Problema Observado

Na primeira evidência adversarial da fase 4 (dois ataques em sequência ao mesmo cliente), o `logs/audit.jsonl` registrava os eventos da execução 1 **novamente** durante a execução 2 — ambos os blocos com o mesmo `request_id`:

```text
{"request_id": "ee7034263d28", "event": "security_blocked", "kind": "injection", ...}   ← 1ª execução
...
{"request_id": "ee7034263d28", "event": "security_blocked", "kind": "destructive", ...} ← 2ª execução, mesmo request_id!
```

Causa: com o `MemorySaver` (checkpointer por thread) + reducer `operator.add` em `audit_events`, o estado **acumula** os eventos de todas as execuções do thread. O `run_recommendation` escrevia a lista acumulada inteira com o `request_id` da execução atual — correlação cruzada que invalidaria a investigação de execuções (critério 11).

## Alteração Realizada

1. `_audit(state, event, ...)` agora inclui o `request_id` da execução **dentro de cada evento** (`app/graph/nodes.py`)
2. `run_recommendation` **filtra** os eventos pelo `request_id` da execução corrente antes de persistir (`app/graph/builder.py`)

```python
events = [
    event for event in result.get("audit_events", [])
    if event.get("request_id") == request_id
]
```

## Resultado Obtido

Segunda rodada da evidência adversarial: exatamente 4 eventos por execução, cada bloco com seu próprio `request_id` (`f7a02470c9e1` e `9bc57996b102`) — correlação 1:1 entre execução e registro de auditoria. Suite: 34 passed.

## Evidência

- [`../../evidencias/seguranca/adversarial-fase-4.md`](../../evidencias/seguranca/adversarial-fase-4.md) (antes e depois)
- Arquivos: `app/graph/nodes.py`, `app/graph/builder.py`
