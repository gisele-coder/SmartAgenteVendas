---
origem: sessão de desenvolvimento assistido (opencode)
status: oficial
data: 2026-08-29
fase: 3 — API FastAPI + Memória
---

# Fase 3 — API FastAPI + Memória

> Objetivo: expor o agente como API local com contrato estruturado, `request_id` por execução e memória de curto prazo via checkpointer (brief 4.4).

---

## Prompts utilizados

1. **Aprovação de continuidade:**
   > "sim" — aprovação da execução da Parte 3 conforme plano (`docs/plano-execucao.md`), com a regra permanente de registro de prompts por fase

---

## Resultado da interação

### Implementação
- `app/main.py`: `POST /recomendacoes` (request/response Pydantic), `GET /health` com modelo vigente; **injeção de dependência** do LLM (`Annotated[ChatOpenAI, Depends(get_llm_service)]`) — permite override nos testes sem rede nem custo; `request_id` = `uuid4().hex[:12]` por execução
- `app/graph/builder.py`: `graph.compile(checkpointer=MemorySaver())`; `run_recommendation` usa `thread_id = "customer-<id>"` — **memória por cliente** entre execuções (brief 4.4: checkpointer)
- `app/graph/nodes.py`: `validate_input` captura as recomendações da execução anterior **antes** de sobrescrever → `previous_recommendations` (memória demonstrável na API); campos voláteis (`errors`, `fallback_used`) resetados a cada execução para evitar vazamento entre chamadas do mesmo thread
- `app/schemas.py`: `RecommendationResponse` ganhou `previous_recommendations` e `reason` (motivo do bloqueio)

### Bugs/correções durante a execução
1. `RecommendationResponse` descartava o campo `reason` do bloqueio (response_model filtra campos não declarados) → campo `reason` adicionado ao contrato
2. Artefato de digitação em `schemas.py` (`default_factory=dict if False else list`) corrigido no mesmo ciclo
3. `test_health` atualizado para o novo contrato do `/health` (inclui `model`)

### Justificativa da estratégia de memória (brief 4.4)
- **Memória de curto prazo**: `MemorySaver` (checkpointer em memória) com thread por cliente — persiste estado entre execuções e habilita `previous_recommendations`
- **Contexto externo**: histórico de pedidos + coocorrência via tools (fonte xlsx), documentado no README e `system.md`
- RAG vetorial não é necessário no domínio atual (base pequena, consulta por cliente); registrado como evolução futura

---

## Evidências

| Evidência | Detalhe |
|---|---|
| Testes | `pytest` → **24 passed** (7 novos em `test_api.py`: integração HTTP, memória entre chamadas, injection via API, cliente inexistente, 422, fallback via API) |
| Lint | `ruff check .` → All checks passed |
| Smoke real | uvicorn + `curl`: `POST /recomendacoes` → 200 com JSON completo e justificativas do LLM real — registrado em [`docs/evidencias/execucoes/api-668b104164e6-fase-3.md`](../../evidencias/execucoes/api-668b104164e6-fase-3.md) |
| Branch | `feature/api-memoria` |
