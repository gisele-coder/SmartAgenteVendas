# Refinamentos — Histórico

> Cada arquivo registra um ciclo completo: **problema observado → alteração realizada → resultado obtido**, conforme exigido pelo brief (seção 4.10 / critério 15).

| Arquivo | Data | Resumo |
|---|---|---|
| [`refinamento-1-max-tokens.md`](./refinamento-1-max-tokens.md) | 2026-08-29 | Modelo de reasoning consumia todo o `max_tokens` sem gerar JSON → folga de tokens + validação/fallback |
| [`refinamento-2-audit-correlacao.md`](./refinamento-2-audit-correlacao.md) | 2026-08-29 | Checkpointer acumulava `audit_events` entre execuções do thread → filtro por `request_id` no persistir |
| [`refinamento-3-chatflow-para-agentflow-v2.md`](./refinamento-3-chatflow-para-agentflow-v2.md) | 2026-08-31 | Custom JS Function de Chatflow v3.x rejeita Chat Model (erro de JSON ao conectar) → migração do fluxo para Agentflow V2 (`Start → LLM → Custom Function`); demo E2E real `3bfceacea49f` (Discord HTTP 204) |
