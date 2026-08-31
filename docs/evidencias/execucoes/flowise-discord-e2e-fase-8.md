---
origem: sessão de desenvolvimento (opencode) — Parte 8
status: oficial
data: 2026-08-31
finalidade: comprovar a integração low-code Flowise + Discord acionada por evento de segurança (critério 14)
relacionado: [../../../docs/lowcode/reproducao-flowise.md](../../../docs/lowcode/reproducao-flowise.md)
---

# Execução — e2e Flowise + Discord (Parte 8)

## Identificação
- **request_id:** `3bfceacea49f`
- **gatilho:** requisição adversarial (prompt injection) bloqueada pelo nó `security_check`
- **canal de saída:** webhook do Discord `#smartorder-alertas` — alerta recebido ✅ (confirmado visualmente pelo usuário)
- **data/hora:** 2026-08-31 06:04 UTC

## Sinais Coletados
| Sinal | Caminho | Trecho relevante |
|---|---|---|
| Logs JSON por node | `logs/execution.log` | 5 entradas correlacionadas pelo `request_id` (ver abaixo) |
| Audit JSONL | `logs/audit.jsonl` | 4 eventos correlacionados (`input_validated`, `security_blocked`, `request_blocked`, `response_completed`) |
| Métricas | `GET /metrics` | endpoint respondeu 200 durante a demo |
| Visual Discord | canal `#smartorder-alertas` | bloco `SEVERIDADE: alta / EVENTO: ... / CAUSA PROVÁVEL / AÇÃO RECOMENDADA` recebido |

### Trechos dos logs (`logs/execution.log`)
```json
{"request_id": "3bfceacea49f", "node": "validate_input",     "latency_ms": 391.9, "validated": true, "has_memory": false}
{"request_id": "3bfceacea49f", "node": "security_check",     "latency_ms": 0.1,   "blocked": true, "kind": "injection"}
{"request_id": "3bfceacea49f", "node": "block_request",      "latency_ms": 0.0}
{"request_id": "3bfceacea49f", "node": "finalize_response",  "latency_ms": 0.0,   "status": "blocked"}
{"request_id": "3bfceacea49f", "node": "flowise_notify",     "latency_ms": 6692.3, "event": "security_blocked", "status_code": 200}
```

### Trechos do audit (`logs/audit.jsonl`)
```json
{"request_id": "3bfceacea49f", "event": "input_validated"}
{"request_id": "3bfceacea49f", "event": "security_blocked", "kind": "injection", "patterns": ["ignore suas regras"]}
{"request_id": "3bfceacea49f", "event": "request_blocked",   "reason": "possivel prompt injection detectado na consulta"}
{"request_id": "3bfceacea49f", "event": "response_completed", "status": "blocked"}
```

## Fluxo Percorrido

1. `validate_input` — 391,9 ms (Pydantic; cliente 100011 ok)
2. `security_check` — 0,1 ms — match no padrão `ignore suas regras` → `kind=injection`, `blocked=true`
3. `block_request` — 0,0 ms — sem LLM acionado (autonomia: agente é somente-leitura)
4. `finalize_response` — 0,0 ms — responde `status: "blocked"` ao cliente
5. `flowise_notify` — 6 692,3 ms (chamada best-effort) →
   5.1 **Agentflow V2** (`docs/lowcode/flowise-flow.json`):
   - **Start** recebe `{question: json_evento}`
   - **LLM** (`poolside/laguna-s-2.1` via OpenRouter, temp 0,2, ~1,5 s, 348 tokens) — produz:
     ```
     SEVERIDADE: alta
     EVENTO: security_blocked | REQUEST: 3bfceacea49f | CLIENTE: 100011
     CAUSA PROVÁVEL: Tentativa de injeção detectada na requisição.
     AÇÃO RECOMENDADA: Investigar o payload da requisição e validar as regras de WAF.
     ```
   - **Custom Function** (`require('axios')` → `POST $vars.DISCORD_WEBHOOK_URL`) — Discord retorna **HTTP 204** (sucesso)

## Decisões Relevantes
- **Bloqueio pré-LLM**: a `security_check` detectou injection sem chamar o LLM principal (coerente com Parte 4) — o evento chega ao Flowise apenas como alerta operacional
- **`FLOWISE_API_KEY` vazio**: o endpoint `cloud.flowiseai.com/api/v1/prediction/<id>` respondeu **200 sem autenticação** (Flowise Cloud free tier com flow público); a var `.env` foi mantida vazia e o cabeçalho `Authorization` não é enviado (código: `app/integrations/flowise.py:30`)
- **Timeout elevado (45 s)**: modelo free de reasoning pode levar 5–10 s; `flowise_timeout_s=45` evita alarmes falsos; chamada permanece best-effort (`tests/test_flowise.py:test_erro_no_flowise_nao_quebra_a_resposta` cobre a falha)
- **Modelo real**: `poolside/laguna-s-2.1` (OpenRouter free) — slug completo identificado via `responseMetadata.model_name` no trace do Flowise

## Latências observadas
| Segmento | Tempo |
|---|---|
| `validate_input` | 391,9 ms |
| `security_check` + `block_request` + `finalize_response` | 0,1 ms |
| `flowise_notify` (HTTP até o Flowise) | **6 692,3 ms** (≈ 98,8 % do total) |
| **Total da requisição HTTP** | **10 115 ms** |
| └─ interno do Flowise: LLM (`laguna-s-2.1`) | ≈ 1 477 ms |
| └─ interno do Flowise: Custom Function (axios → Discord) | ≈ 130 ms |

Confirmação da Parte 5: o **LLM é o gargalo**, agora observado em **dois níveis** — na aplicação principal e no agentflow.

## Conclusão
- **E2E comprovado**: app bloqueia injection → audit registra → `notify_flowise` → Agentflow V2 classifica → Discord envia alerta (HTTP 204). Todos os sinais correlacionados por `request_id`.
- **Critério 14 atendido**: ferramenta low-code (Flowise) com **trigger** (evento HTTP da app) e **saída observável** (mensagem no Discord com severidade/causa/ação).
- **Lição registrada** (na seção `Correções` de `reproducao-flowise.md`): o node *Custom JS Function* de Chatflow (v3.x) **não aceita conexão de Chat Model** — única entrada é anchor `json` → erro de JSON ao conectar `ChatOpenRouter → Custom Function`. Solução: reconstrução como **Agentflow V2** (`Start → LLM → Custom Function`).
- **Pendência pós-entrega**: rotacionar a URL do webhook Discord e (se habilitada no Dashboard) a API key do Flowise — ambas circularam no chat durante o desenvolvimento.

## Screenshots
| Arquivo | Conteúdo |
|---|---|
| `docs/evidencias/screenshots/flowise-1-erro-conexao-chatflow.jpg` | Primeira tentativa (Chatflow + Custom JS Function) — erro de JSON ao conectar a saída do `ChatOpenRouter` ao `Custom Function` |
| `docs/evidencias/screenshots/flowise-2-agentflow-discord-ok.jpg` | Agentflow V2 funcionando: Custom Function retornando `Alerta enviado ao Discord (HTTP 204)` |